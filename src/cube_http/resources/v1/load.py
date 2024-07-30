from typing import Optional

from ...exc import LoadV1Error
from ...types.v1.load import (
    V1LoadRequest,
    V1LoadRequestQuery,
    V1LoadResponse,
    V1LoadRequestQueryDict,
)
from ..._utils.serde import model_parse, model_dict

from .._base import AsyncApiResource, SyncApiResource

__all__ = ["Load", "AsyncLoad"]


class Load(SyncApiResource):
    def __call__(
        self,
        *,
        query: Optional[V1LoadRequestQueryDict] = None,
    ) -> V1LoadResponse:
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
        req = self._client.build_request(
            "POST",
            "/v1/load",
            json=model_dict(
                V1LoadRequest(
                    queryType="multi",
                    query=model_parse(V1LoadRequestQuery, query),
                ),
                exclude_none=True,
            ),
        )
        res = self._client.send(req)
        if res.status_code == 200:
            return model_parse(V1LoadResponse, res.json())
        else:
            raise LoadV1Error.from_response(res)


class AsyncLoad(AsyncApiResource):
    async def __call__(
        self,
        *,
        query: Optional[V1LoadRequestQueryDict] = None,
    ) -> V1LoadResponse:
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
        req = self._client.build_request(
            "POST",
            "/v1/load",
            json=model_dict(
                V1LoadRequest(
                    queryType="multi",
                    query=model_parse(V1LoadRequestQuery, query),
                ),
                exclude_none=True,
            ),
        )
        res = await self._client.send(req)
        if res.status_code == 200:
            return model_parse(V1LoadResponse, res.json())
        else:
            raise LoadV1Error.from_response(res)
