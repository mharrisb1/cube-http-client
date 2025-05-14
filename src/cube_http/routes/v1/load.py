from typing import TypeVar, overload

from ...exc import V1LoadError
from ...types.v1.load_request import V1LoadRequest
from ...types.v1.load_response import V1LoadResponse
from .._base import AsyncRoute, SyncRoute

T = TypeVar("T", bound=V1LoadResponse)


class SyncLoadRoute(SyncRoute):
    @overload
    def load(
        self, request: V1LoadRequest, *, response_model: None = None
    ) -> V1LoadResponse: ...

    @overload
    def load(self, request: V1LoadRequest, *, response_model: type[T]) -> T: ...

    def load(
        self, request: V1LoadRequest, *, response_model: type[T] | None = None
    ) -> T | V1LoadResponse:
        """
        Execute a load query.

        Args:
            request: The load request parameters
            response_model: Optional custom response model class to use instead of the default
                            Must inherit from `V1LoadResponse` model.

        Returns:
            The response model instance

        Raises:
            V1LoadError: If the request failed
        """
        res = self._post("/v1/load", request | {"queryType": "multi"})
        if res.status_code == 200:
            if response_model is not None:
                return response_model.from_response(res)
            return V1LoadResponse.from_response(res)
        else:
            raise V1LoadError.from_response(res)


class AsyncLoadRoute(AsyncRoute):
    @overload
    async def load(
        self, request: V1LoadRequest, *, response_model: None = None
    ) -> V1LoadResponse: ...

    @overload
    async def load(
        self, request: V1LoadRequest, *, response_model: type[T]
    ) -> T: ...

    async def load(
        self, request: V1LoadRequest, *, response_model: type[T] | None = None
    ) -> T | V1LoadResponse:
        """
        Execute a load query asynchronously.

        Args:
            request: The load request parameters
            response_model: Optional custom response model class to use instead of the default
                            Must inherit from `V1LoadResponse` model.

        Returns:
            The response model instance

        Raises:
            V1LoadError: If the request failed
        """
        res = await self._post("/v1/load", request | {"queryType": "multi"})
        if res.status_code == 200:
            if response_model is not None:
                return response_model.from_response(res)
            return V1LoadResponse.from_response(res)
        else:
            raise V1LoadError.from_response(res)
