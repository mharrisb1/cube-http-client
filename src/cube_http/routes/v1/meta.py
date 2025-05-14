from ...exc import V1MetaError
from ...types.v1.meta_request import V1MetaRequest
from ...types.v1.meta_response import V1MetaResponse
from .._base import AsyncRoute, SyncRoute


class SyncMetaRoute(SyncRoute):
    def meta(self, reqeust: V1MetaRequest | None = None) -> V1MetaResponse:
        res = self._get("/v1/meta", params=reqeust or {})
        if res.status_code == 200:
            return V1MetaResponse.from_response(res)
        else:
            raise V1MetaError.from_response(res)


class AsyncMetaRoute(AsyncRoute):
    async def meta(self, reqeust: V1MetaRequest | None = None) -> V1MetaResponse:
        res = await self._get("/v1/meta", params=reqeust or {})
        if res.status_code == 200:
            return V1MetaResponse.from_response(res)
        else:
            raise V1MetaError.from_response(res)
