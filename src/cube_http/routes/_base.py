from typing import Any, Literal, Mapping

import httpx


class SyncRoute:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def _build_request(
        self,
        method: Literal["GET", "POST"],
        route: str,
        *,
        params: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
    ) -> httpx.Request:
        return self._client.build_request(
            method, route, params=params, json=body
        )

    def _get(
        self, route: str, params: Mapping[str, Any] | None = None
    ) -> httpx.Response:
        req = self._build_request("GET", route, params=params)
        return self._client.send(req)

    def _post(
        self, route: str, body: Mapping[str, Any] | None = None
    ) -> httpx.Response:
        req = self._build_request("POST", route, body=body)
        return self._client.send(req)


class AsyncRoute:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    def _build_request(
        self,
        method: Literal["GET", "POST"],
        route: str,
        *,
        params: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
    ) -> httpx.Request:
        return self._client.build_request(
            method, route, params=params, json=body
        )

    async def _get(
        self, route: str, params: Mapping[str, Any] | None = None
    ) -> httpx.Response:
        req = self._build_request("GET", route, params=params)
        return await self._client.send(req)

    async def _post(
        self, route: str, body: Mapping[str, Any] | None = None
    ) -> httpx.Response:
        req = self._build_request("POST", route, body=body)
        return await self._client.send(req)
