from typing import Any

from pydantic import BaseModel, Field

from .._base import ResponseModel


class V1SqlResult(BaseModel):
    sql: tuple[str, list[str]] = Field(
        description="Formatted SQL query with parameters"
    )
    alias_name_to_member: dict[str, Any] | None = Field(
        default=None,
        alias="aliasNameToMember",
    )
    member_names: list[str] | None = Field(
        default=None, description="Member names", alias="memberNames"
    )
    cache_key_queries: list[Any] | None = Field(
        default=None, alias="cacheKeyQueries"
    )
    can_use_transform_query: dict[str, Any] | None = Field(
        default=None, alias="canUseTransformedQuery"
    )
    data_source: str | None = Field(default=None, alias="dataSource")
    external: bool | None = Field(default=None)
    lambda_queries: dict[str, Any] | None = Field(
        default=None, alias="lambdaQueries"
    )
    order: dict[str, Any] | None = Field(default=None)
    pre_aggregations: list[Any] | None = Field(
        default=None, alias="preAggregations"
    )
    rollup_match_results: list[Any] | None = Field(
        default=None, alias="rollupMatchResults"
    )


class V1SqlResponse(ResponseModel):
    sql: V1SqlResult = Field(description="SQL response object")
