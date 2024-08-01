from typing import Optional

from ...exc import LoadV1Error, MetaV1Error
from ...types.v1.meta import V1MetaResponse
from ...types.v1.load import (
    V1LoadRequestQueryDict,
    V1LoadResponse,
    V1LoadRequest,
    V1LoadRequestQuery,
)
from ..._utils.serde import model_dict, model_parse

from .._base import SyncApiResources, AsyncApiResources


class V1Resources(SyncApiResources):
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

    def load(
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
                by_alias=True,
            ),
        )
        res = self._client.send(req)
        if res.status_code == 200:
            return model_parse(V1LoadResponse, res.json())
        else:
            raise LoadV1Error.from_response(res)


class AsyncV1Resources(AsyncApiResources):
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

    async def load(
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
                by_alias=True,
            ),
        )
        res = await self._client.send(req)
        if res.status_code == 200:
            return model_parse(V1LoadResponse, res.json())
        else:
            raise LoadV1Error.from_response(res)
