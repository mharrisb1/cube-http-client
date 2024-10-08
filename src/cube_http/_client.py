from functools import cached_property
from typing import Optional, Type, Union

import httpx

from .exc.v1 import V1MetaError, V1LoadError, V1SqlError

from .types._client import ClientOptions
from .types._generics import THttpClient
from .types.v1.load import (
    V1LoadRequestQuery,
    V1LoadRequestQueryDict,
    V1LoadResponse,
    V1LoadRequest,
)
from .types.v1.meta import V1MetaResponse
from .types.v1.sql import V1SqlRequest, V1SqlResponse

__all__ = ["Client", "AsyncClient"]


class BaseClient:
    def __init__(
        self,
        client: Type[THttpClient],
        transport: Union[
            Type[httpx.HTTPTransport], Type[httpx.AsyncHTTPTransport]
        ],
        options: ClientOptions[THttpClient],
    ) -> None:
        headers = {
            "Authorization": options["token"],
            "Content-Type": "application/json",
        }
        headers |= options.get("default_headers", {})

        self._client = options.get("http_client") or client(
            base_url=options["url"],
            headers=headers,
            timeout=options.get("timeout"),
            transport=transport(retries=options.get("max_retries", 0)),  # type: ignore
        )


class Client(BaseClient):
    """Synchronous HTTP client"""

    _client: httpx.Client

    def __init__(self, options: ClientOptions[httpx.Client]) -> None:
        super().__init__(httpx.Client, httpx.HTTPTransport, options)

    @cached_property
    def v1(self) -> "_V1":
        return Client._V1(self._client)

    class _V1:
        """
        Endpoint wrapper
        """

        def __init__(self, client: httpx.Client) -> None:
            self._client = client

        def meta(
            self,
            *,
            extended: Optional[bool] = None,
        ) -> V1MetaResponse:
            """
            Load metadata.

            Parameters:
                extended: You will receive extended response if this parameter is true

            Returns:
                V1MetaResponse: The response of the load metadata request

            Raises:
                MetaV1Error: If the request could not be completed or an internal service error
            """
            params = {"extended": extended} if extended is not None else {}
            req = self._client.build_request("GET", "/v1/meta", params=params)
            res = self._client.send(req)
            if res.status_code == 200:
                return V1MetaResponse.from_response(res)
            raise V1MetaError.from_response(res)

        def load(self, query: V1LoadRequestQueryDict) -> V1LoadResponse:
            """
            Load data via Cube JSON Query.

            Parameters:
                query: Cube query

            Returns:
                V1LoadResponse: The response of the load request

            Raises:
                LoadV1Error: If the request could not be completed or an internal service error
            """
            body = V1LoadRequest.build(query).as_request_body()
            req = self._client.build_request("POST", "/v1/load", json=body)
            res = self._client.send(req)
            if res.status_code == 200:
                return V1LoadResponse.from_response(res)
            raise V1LoadError.from_response(res)

        def sql(
            self,
            query: Union[V1LoadRequestQueryDict, V1LoadRequestQuery],
        ) -> V1SqlResponse:
            """
            Get the SQL Code generated by Cube to be executed in the database.

            Parameters:
                query: Cube query

            Returns:
                V1SqlResponse: The response of the sql request

            Raises:
                V1SqlError: If the request could not be completed or an internal service error
            """
            body = V1SqlRequest.build(query).as_request_body()
            req = self._client.build_request("POST", "/v1/sql", json=body)
            res = self._client.send(req)
            if res.status_code == 200:
                return V1SqlResponse.from_response(res)
            raise V1SqlError.from_response(res)


class AsyncClient(BaseClient):
    """Asynchronous HTTP client"""

    _client: httpx.AsyncClient

    def __init__(self, options: ClientOptions[httpx.AsyncClient]) -> None:
        super().__init__(httpx.AsyncClient, httpx.AsyncHTTPTransport, options)

    @cached_property
    def v1(self):
        return AsyncClient._V1(self._client)

    class _V1:
        """
        Endpoint wrapper
        """

        def __init__(self, client: httpx.AsyncClient) -> None:
            self._client = client

        async def meta(
            self,
            *,
            extended: Optional[bool] = None,
        ) -> V1MetaResponse:
            """
            Load metadata.

            Parameters:
                extended: You will receive extended response if this parameter is true

            Returns:
                V1MetaResponse: The response of the load metadata request

            Raises:
                MetaV1Error: If the request could not be completed or an internal service error
            """
            params = {"extended": extended} if extended is not None else {}
            req = self._client.build_request("GET", "/v1/meta", params=params)
            res = await self._client.send(req)
            if res.status_code == 200:
                return V1MetaResponse.from_response(res)
            raise V1MetaError.from_response(res)

        async def load(self, query: V1LoadRequestQueryDict) -> V1LoadResponse:
            """
            Load data via Cube JSON Query.

            Parameters:
                query: Either a single URL encoded Cube Query, or an array of queries
                query_type: If multiple queries are passed in query for data blending, this must be set to `multi`

            Returns:
                V1LoadResponse: The response of the load request

            Raises:
                LoadV1Error: If the request could not be completed or an internal service error
            """
            body = V1LoadRequest.build(query).as_request_body()
            req = self._client.build_request("POST", "/v1/load", json=body)
            res = await self._client.send(req)
            if res.status_code == 200:
                return V1LoadResponse.from_response(res)
            raise V1LoadError.from_response(res)

        async def sql(
            self,
            query: Union[V1LoadRequestQueryDict, V1LoadRequestQuery],
        ) -> V1SqlResponse:
            """
            Get the SQL Code generated by Cube to be executed in the database.

            Parameters:
                query: Cube query

            Returns:
                V1SqlResponse: The response of the sql request

            Raises:
                V1SqlError: If the request could not be completed or an internal service error
            """
            body = V1SqlRequest.build(query).as_request_body()
            req = self._client.build_request("POST", "/v1/sql", json=body)
            res = await self._client.send(req)
            if res.status_code == 200:
                return V1SqlResponse.from_response(res)
            raise V1SqlError.from_response(res)
