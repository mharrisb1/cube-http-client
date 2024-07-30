from typing import Optional

from ...exc import MetaV1Error
from ...types.v1.meta import V1MetaResponse
from ..._utils.serde import model_parse

from .._base import AsyncApiResource, SyncApiResource

__all__ = ["Meta", "AsyncMeta"]


class Meta(SyncApiResource):
    def __call__(
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
        req = self._client.build_request(
            "GET",
            "/v1/meta",
            params={"extended": extended},
        )
        res = self._client.send(req)
        if res.status_code == 200:
            return model_parse(V1MetaResponse, res.json())
        else:
            raise MetaV1Error.from_response(res)


class AsyncMeta(AsyncApiResource):
    async def __call__(
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
        req = self._client.build_request(
            "GET",
            "/v1/meta",
            params={"extended": extended},
        )
        res = await self._client.send(req)
        if res.status_code == 200:
            return model_parse(V1MetaResponse, res.json())
        else:
            raise MetaV1Error.from_response(res)
