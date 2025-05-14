from typing import Any

from pydantic import BaseModel, Field

from .._base import ResponseModel


class V1LoadResultAnnotation(BaseModel):
    measures: dict[str, dict[str, Any]] = Field(
        description="Annotations for measures in the result."
    )

    dimensions: dict[str, dict[str, Any]] = Field(
        description="Annotations for dimensions in the result."
    )

    segments: dict[str, dict[str, Any]] = Field(
        description="Annotations for segments in the result."
    )

    time_dimensions: dict[str, dict[str, Any]] = Field(
        alias="timeDimensions",
        description="Annotations for time dimensions in the result.",
    )


class V1LoadResult(BaseModel):
    query: dict[str, Any] | None = Field(
        default=None, description="The original query object."
    )

    data: list[dict[str, Any]] = Field(
        description="Data returned by the load result."
    )

    last_refresh_time: str | None = Field(
        alias="lastRefreshTime",
        default=None,
        description="Timestamp indicating the last time the query was refreshed.",
    )

    refresh_key_values: list[list[dict[str, Any]]] | None = Field(
        alias="refreshKeyValues",
        default=None,
        description="Values of the refresh key used for the query.",
    )

    used_pre_aggregations: dict[str, Any] | None = Field(
        alias="usedPreAggregations",
        default=None,
        description="Information on pre-aggregations used in the query.",
    )

    transformed_query: dict[str, Any] | None = Field(
        alias="transformedQuery",
        default=None,
        description="The query after being transformed, usually for optimization purposes.",
    )

    request_id: str | None = Field(
        alias="requestId",
        default=None,
        description="Unique identifier for the request.",
    )

    annotation: V1LoadResultAnnotation = Field(
        description="Annotations for the load result."
    )

    data_source: str | None = Field(
        alias="dataSource",
        default=None,
        description="The data source from which the result was loaded.",
    )

    db_type: str | None = Field(
        alias="dbType", default=None, description="The type of database queried."
    )

    ext_db_type: str | None = Field(
        alias="exDbType",
        default=None,
        description="External database type, if applicable.",
    )

    external: bool | None = Field(
        default=None,
        description="Indicates if the query result was fetched from an external source.",
    )

    slow_query: bool | None = Field(
        alias="slowQuery",
        default=None,
        description="Indicates if the query is considered slow.",
    )


class V1LoadResponse(ResponseModel):
    pivot_query: dict[str, Any] | None = Field(
        alias="pivotQuery",
        default=None,
        description="The pivot query associated with the load response.",
    )

    query_type: str | None = Field(
        alias="queryType",
        default=None,
        description="Type of the query, primarily for internal use.",
    )

    slow_query: bool | None = Field(
        alias="slowQuery",
        default=None,
        description="Indicates if the query was considered slow.",
    )

    results: list[V1LoadResult] = Field(
        description="list of results obtained from the load response."
    )
