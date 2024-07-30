from functools import cached_property

import httpx

from .resources import V1, AsyncV1
from .types._client import ClientOptions, AsyncClientOptions


class Client:
    """Synchronous HTTP client"""

    def __init__(self, options: ClientOptions) -> None:
        headers = {
            "Authorization": options["token"],
            "Content-Type": "application/json",
        }
        headers |= options.get("default_headers", {})

        self._client = options.get("http_client") or httpx.Client(
            base_url=options["url"],
            headers=headers,
            timeout=options.get("timeout"),
            transport=httpx.HTTPTransport(
                retries=options.get("max_retries", 0),
            ),
        )

    @cached_property
    def v1(self) -> V1:
        return V1(self._client)


class AsyncClient:
    """Asynchronous HTTP client"""

    _client: httpx.AsyncClient

    def __init__(self, options: AsyncClientOptions) -> None:
        headers = {"Authorization": options["token"]}
        headers |= options.get("default_headers", {})

        self._client = options.get("http_client") or httpx.AsyncClient(
            base_url=options["url"],
            headers=headers,
            timeout=options.get("timeout"),
            transport=httpx.AsyncHTTPTransport(
                retries=options.get("max_retries", 0),
            ),
        )

    @cached_property
    def v1(self) -> AsyncV1:
        return AsyncV1(self._client)
