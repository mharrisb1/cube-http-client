from functools import cached_property
from typing import Any, Mapping, TypedDict

import httpx
from typing_extensions import NotRequired, Required

from .routes.v1 import AsyncV1Routes, SyncV1Routes


class BaseClientOptions(TypedDict):
    token: Required[str]
    """API token used to authorize requests and determine SQL database you're accessing"""

    url: Required[str]
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


class Client:
    def __init__(
        self,
        options: ClientOptionsLike,
    ) -> None:
        headers = {
            "Authorization": options["token"],
            "Content-Type": "application/json",
        }
        headers |= options.get("default_headers", {})
        self._http_client = options.get("http_client") or httpx.Client(
            base_url=options["url"],
            headers=headers,
            timeout=options.get("timeout"),
            transport=httpx.HTTPTransport(retries=options.get("max_retries", 0)),
        )

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
        self._http_client.close()

    @cached_property
    def v1(self) -> SyncV1Routes:
        return SyncV1Routes(self._http_client)


class AsyncClient:
    def __init__(
        self,
        options: AsyncClientOptionsLike,
    ) -> None:
        headers = {
            "Authorization": options["token"],
            "Content-Type": "application/json",
        }
        headers |= options.get("default_headers", {})
        self._http_client = options.get("http_client") or httpx.AsyncClient(
            base_url=options["url"],
            headers=headers,
            timeout=options.get("timeout"),
            transport=httpx.AsyncHTTPTransport(
                retries=options.get("max_retries", 0)
            ),
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
        await self._http_client.aclose()

    @cached_property
    def v1(self) -> AsyncV1Routes:
        return AsyncV1Routes(self._http_client)
