from functools import cached_property
from typing import Any, Generic, Mapping, TypedDict, TypeVar, cast

import httpx
from typing_extensions import NotRequired

from .routes.v1 import AsyncV1Routes, SyncV1Routes


class BaseClientOptions(TypedDict, total=False):
    token: str
    """API token used to authorize requests and determine SQL database you're accessing"""

    url: str
    """Deployment base URL"""

    timeout: NotRequired[float | httpx.Timeout]
    """Timeout configuration to use when sending requests"""

    max_retries: NotRequired[int]
    """Maximum number of retries to attempt on failed requests. Defaults to 0 for no retries"""

    default_headers: NotRequired[Mapping[str, str]]
    """Default headers to add to every request"""


class ClientOptions(BaseClientOptions):
    http_client: NotRequired[httpx.Client]
    """Optional HTTPX client to use for requests"""


class AsyncClientOptions(BaseClientOptions):
    http_client: NotRequired[httpx.AsyncClient]
    """Optional HTTPX client to use for requests"""


ClientOptionsLike = ClientOptions | dict[str, Any]
AsyncClientOptionsLike = AsyncClientOptions | dict[str, Any]


def _extract_token_from_headers(headers: httpx.Headers) -> str | None:
    auth_header = headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    return auth_header


_O = TypeVar("_O", bound=dict[str, Any])
_C = TypeVar("_C", bound=httpx.Client | httpx.AsyncClient)
_T = TypeVar("_T", bound=httpx.HTTPTransport | httpx.AsyncHTTPTransport)
_R = TypeVar("_R", bound=SyncV1Routes | AsyncV1Routes)


def _get_merged_client_options(
    options: _O,
    http_client: httpx.Client | httpx.AsyncClient,
) -> _O:
    merged_options = cast(_O, options.copy())
    merged_options["url"] = merged_options.get("url", str(http_client.base_url))
    merged_options["token"] = merged_options.get(
        "token", _extract_token_from_headers(http_client.headers) or ""
    )
    merged_options["timeout"] = merged_options.get(
        "timeout", http_client.timeout
    )

    return merged_options


class BaseClient(Generic[_C, _T, _R]):
    """Base class with shared logic for both sync and async clients."""

    _http_client: _C

    def __init__(
        self,
        options: dict[str, Any],
        client_class: type[_C],
        transport_class: type[_T],
    ) -> None:
        # Extract the custom client if provided
        http_client = options.get("http_client")

        if http_client:
            # Use provided client with merged options
            self._setup_with_custom_client(options, http_client)
        else:
            # Create a new client with provided options
            self._setup_new_client(options, client_class, transport_class)

    def _setup_with_custom_client(
        self,
        options: dict[str, Any],
        http_client: httpx.Client | httpx.AsyncClient,
    ) -> None:
        # Merge options from the client with explicit options
        options = _get_merged_client_options(options, http_client)

        # Validate required options
        self._validate_required_options(options, custom_client=True)

        # Store the custom client
        self._http_client = cast(_C, http_client)

        # Update client configuration as needed
        self._configure_client(options, http_client)

    def _setup_new_client(
        self,
        options: dict[str, Any],
        client_class: type[_C],
        transport_class: type[_T],
    ) -> None:
        # Validate required options when creating a new client
        self._validate_required_options(options, custom_client=False)

        # Create standard headers
        headers = self._create_headers(options)

        # Create a new client instance
        self._http_client = client_class(
            base_url=options.get("url", ""),
            headers=headers,
            timeout=options.get("timeout"),
            transport=transport_class(retries=options.get("max_retries", 0)),  # type: ignore
        )

    def _validate_required_options(
        self,
        options: dict[str, Any],
        custom_client: bool,
    ) -> None:
        # Check if URL is provided
        if not options.get("url"):
            source = (
                "either in options or in the custom HTTP client"
                if custom_client
                else "in options when not using a custom HTTP client"
            )
            raise ValueError(f"Base URL must be provided {source}")

        # Check if token is provided
        if not options.get("token"):
            source = (
                "either in options or in the custom HTTP client's Authorization header"
                if custom_client
                else "in options when not using a custom HTTP client"
            )
            raise ValueError(f"API token must be provided {source}")

    def _create_headers(self, options: dict[str, Any]) -> dict[str, str]:
        # Create standard headers with authorization and content type
        headers = {
            "Authorization": options.get("token", ""),
            "Content-Type": "application/json",
        }

        # Add any custom headers
        if default_headers := options.get("default_headers"):
            headers |= default_headers

        return headers

    def _configure_client(
        self,
        options: dict[str, Any],
        http_client: httpx.Client | httpx.AsyncClient,
    ) -> None:
        # Set base URL if not already set
        if http_client.base_url == httpx.URL("") and options.get("url"):
            http_client.base_url = httpx.URL(options.get("url", ""))

        # Add authorization header if not present
        if "authorization" not in {
            k.lower() for k in http_client.headers
        } and options.get("token"):
            http_client.headers["Authorization"] = options.get("token", "")

        # Add content-type if not present
        if "content-type" not in {k.lower() for k in http_client.headers}:
            http_client.headers["Content-Type"] = "application/json"

        # Add any custom headers if not already present
        if default_headers := options.get("default_headers"):
            for key, value in default_headers.items():
                if key.lower() not in {k.lower() for k in http_client.headers}:
                    http_client.headers[key] = value


class Client(BaseClient[httpx.Client, httpx.HTTPTransport, SyncV1Routes]):
    """Synchronous HTTP client for the Cube.dev REST API."""

    def __init__(self, options: ClientOptionsLike) -> None:
        super().__init__(dict(options), httpx.Client, httpx.HTTPTransport)

    def __enter__(self) -> "Client":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self.http_client.close()

    @property
    def http_client(self) -> httpx.Client:
        return self._http_client

    @cached_property
    def v1(self) -> SyncV1Routes:
        return SyncV1Routes(self.http_client)


class AsyncClient(
    BaseClient[httpx.AsyncClient, httpx.AsyncHTTPTransport, AsyncV1Routes]
):
    """Asynchronous HTTP client for the Cube.dev REST API."""

    def __init__(self, options: AsyncClientOptionsLike) -> None:
        super().__init__(
            dict(options), httpx.AsyncClient, httpx.AsyncHTTPTransport
        )

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self.http_client.aclose()

    @property
    def http_client(self) -> httpx.AsyncClient:
        return self._http_client

    @cached_property
    def v1(self) -> AsyncV1Routes:
        return AsyncV1Routes(self.http_client)
