from typing import Any, Dict, List, Optional, Tuple, Union
from cube_http._utils.serde import model_parse
from pydantic import BaseModel, Field

from .._base import RequestModel, ResponseModel
from .load import V1LoadRequestQuery, V1LoadRequestQueryDict


class V1SqlResult(BaseModel):
    sql: Tuple[str, List[str]] = Field(
        description="Formatted SQL query with parameters"
    )
    alias_name_to_member: Optional[Dict[str, Any]] = Field(
        default=None,
        alias="aliasNameToMember",
    )
    cache_key_queries: Optional[List[Any]] = Field(
        default=None, alias="cacheKeyQueries"
    )
    can_use_transform_query: Optional[Dict[str, Any]] = Field(
        default=None, alias="canUseTransformedQuery"
    )
    data_source: Optional[str] = Field(default=None, alias="dataSource")
    external: Optional[bool] = Field(default=None)
    lambda_queries: Optional[Dict[str, Any]] = Field(
        default=None, alias="lambdaQueries"
    )
    order: Optional[Dict[str, Any]] = Field(default=None)
    pre_aggregations: Optional[List[Any]] = Field(
        default=None, alias="preAggregations"
    )
    rollup_match_results: Optional[List[Any]] = Field(
        default=None, alias="rollupMatchResults"
    )


class V1SqlResponse(ResponseModel):
    sql: V1SqlResult = Field(description="SQL response object")


class V1SqlRequest(RequestModel):
    query: V1LoadRequestQuery = Field(description="Cube query")

    @classmethod
    def build(
        cls,
        query: Union[V1LoadRequestQuery, V1LoadRequestQueryDict],
    ) -> "V1SqlRequest":
        if not isinstance(query, V1LoadRequestQuery):
            query = model_parse(V1LoadRequestQuery, query)
        return cls(query=query)
