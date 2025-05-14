from typing import TypeVar, overload

from ...exc import V1SqlError
from ...types.v1.sql_request import V1SqlRequest
from ...types.v1.sql_response import V1SqlResponse
from .._base import AsyncRoute, SyncRoute

T = TypeVar("T", bound=V1SqlResponse)


class SyncSqlRoute(SyncRoute):
    @overload
    def sql(
        self, request: V1SqlRequest, *, response_model: None = None
    ) -> V1SqlResponse: ...

    @overload
    def sql(self, request: V1SqlRequest, *, response_model: type[T]) -> T: ...

    def sql(
        self, request: V1SqlRequest, *, response_model: type[T] | None = None
    ) -> T | V1SqlResponse:
        """
        Execute a SQL query.

        Args:
            request: The SQL request parameters
            response_model: Optional custom response model class to use instead of the default
                            Must inherit from `V1SqlResponse` model.

        Returns:
            The response model instance

        Raises:
            V1SqlError: If the request failed
        """
        res = self._post("/v1/sql", body=request)
        if res.status_code == 200:
            if response_model is not None:
                return response_model.from_response(res)
            return V1SqlResponse.from_response(res)
        else:
            raise V1SqlError.from_response(res)


class AsyncSqlRoute(AsyncRoute):
    @overload
    async def sql(
        self, request: V1SqlRequest, *, response_model: None = None
    ) -> V1SqlResponse: ...

    @overload
    async def sql(
        self, request: V1SqlRequest, *, response_model: type[T]
    ) -> T: ...

    async def sql(
        self, request: V1SqlRequest, *, response_model: type[T] | None = None
    ) -> T | V1SqlResponse:
        """
        Execute a SQL query asynchronously.

        Args:
            request: The SQL request parameters
            response_model: Optional custom response model class to use instead of the default
                            Must inherit from `V1SqlResponse` model.

        Returns:
            The response model instance

        Raises:
            V1SqlError: If the request failed
        """
        res = await self._post("/v1/sql", body=request)
        if res.status_code == 200:
            if response_model is not None:
                return response_model.from_response(res)
            return V1SqlResponse.from_response(res)
        else:
            raise V1SqlError.from_response(res)
