from typing import TypeVar, overload

from ...exc import V1MetaError
from ...types.v1.meta_request import V1MetaRequest
from ...types.v1.meta_response import V1MetaResponse
from .._base import AsyncRoute, SyncRoute

T = TypeVar("T", bound=V1MetaResponse)


class SyncMetaRoute(SyncRoute):
    @overload
    def meta(
        self,
        reqeust: V1MetaRequest | None = None,
        *,
        response_model: None = None,
    ) -> V1MetaResponse: ...

    @overload
    def meta(
        self,
        reqeust: V1MetaRequest | None = None,
        *,
        response_model: type[T],
    ) -> T: ...

    def meta(
        self,
        reqeust: V1MetaRequest | None = None,
        *,
        response_model: type[T] | None = None,
    ) -> T | V1MetaResponse:
        """
        Get metadata.

        Args:
            reqeust: Optional meta request parameters
            response_model: Optional custom response model class to use instead of the default
                            Must inherit from `V1MetaResponse` model.

        Returns:
            The response model instance

        Raises:
            V1MetaError: If the request failed
        """
        res = self._get("/v1/meta", params=reqeust or {})
        if res.status_code == 200:
            if response_model is not None:
                return response_model.from_response(res)
            return V1MetaResponse.from_response(res)
        else:
            raise V1MetaError.from_response(res)


class AsyncMetaRoute(AsyncRoute):
    @overload
    async def meta(
        self,
        reqeust: V1MetaRequest | None = None,
        *,
        response_model: None = None,
    ) -> V1MetaResponse: ...

    @overload
    async def meta(
        self,
        reqeust: V1MetaRequest | None = None,
        *,
        response_model: type[T],
    ) -> T: ...

    async def meta(
        self,
        reqeust: V1MetaRequest | None = None,
        *,
        response_model: type[T] | None = None,
    ) -> T | V1MetaResponse:
        """
        Get metadata asynchronously.

        Args:
            reqeust: Optional meta request parameters
            response_model: Optional custom response model class to use instead of the default
                            Must inherit from `V1MetaResponse` model.

        Returns:
            The response model instance

        Raises:
            V1MetaError: If the request failed
        """
        res = await self._get("/v1/meta", params=reqeust or {})
        if res.status_code == 200:
            if response_model is not None:
                return response_model.from_response(res)
            return V1MetaResponse.from_response(res)
        else:
            raise V1MetaError.from_response(res)
