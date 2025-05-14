from ...exc import V1LoadError
from ...types.v1.load_request import V1LoadRequest
from ...types.v1.load_response import V1LoadResponse
from .._base import AsyncRoute, SyncRoute


class SyncLoadRoute(SyncRoute):
    def load(self, request: V1LoadRequest) -> V1LoadResponse:
        res = self._post("/v1/load", request | {"queryType": "multi"})
        if res.status_code == 200:
            return V1LoadResponse.from_response(res)
        else:
            raise V1LoadError.from_response(res)


class AsyncLoadRoute(AsyncRoute):
    async def load(self, request: V1LoadRequest) -> V1LoadResponse:
        res = await self._post("/v1/load", request | {"queryType": "multi"})
        if res.status_code == 200:
            return V1LoadResponse.from_response(res)
        else:
            raise V1LoadError.from_response(res)
