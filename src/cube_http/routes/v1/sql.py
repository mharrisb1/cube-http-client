from ...exc import V1SqlError
from ...types.v1.sql_request import V1SqlRequest
from ...types.v1.sql_response import V1SqlResponse
from .._base import AsyncRoute, SyncRoute


class SyncSqlRoute(SyncRoute):
    def sql(self, request: V1SqlRequest) -> V1SqlResponse:
        res = self._post("/v1/sql", body=request)
        if res.status_code == 200:
            return V1SqlResponse.from_response(res)
        else:
            raise V1SqlError.from_response(res)


class AsyncSqlRoute(AsyncRoute):
    async def sql(self, request: V1SqlRequest) -> V1SqlResponse:
        res = await self._post("/v1/sql", body=request)
        if res.status_code == 200:
            return V1SqlResponse.from_response(res)
        else:
            raise V1SqlError.from_response(res)
