from typing import Any

from pydantic import BaseModel, Field

from .._base import ResponseModel
from .operators import FilterOperator
from .time_granularities import TimeGranularity


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


class V1LoadRequestQueryFilterBase(BaseModel):
    member: str | None = Field(
        default=None,
        description="Dimension or measure to be used in the filter, e.g., `stories.isDraft`. "
        "Differentiates between filtering dimensions and filtering measures.",
    )

    operator: FilterOperator | None = Field(
        default=None,
        description="Operator to apply in the filter. "
        "Some operators are exclusive to measures, while others depend on the dimension type.",
    )

    values: list[str] | None = Field(
        default=None,
        description="List of values for the filter, provided as strings. "
        "For dates, use the `YYYY-MM-DD` format.",
    )


class V1LoadRequestQueryFilterLogicalOr(BaseModel):
    or_filters: list["V1LoadRequestQueryFilterItem"] | None = Field(
        default=None,
        alias="or",
        description="List of filter items combined with logical OR",
    )


class V1LoadRequestQueryFilterLogicalAnd(BaseModel):
    and_filters: list["V1LoadRequestQueryFilterItem"] | None = Field(
        default=None,
        alias="and",
        description="List of filter items combined with logical AND",
    )


# Forward reference for filter items
V1LoadRequestQueryFilterItem = (
    V1LoadRequestQueryFilterBase
    | V1LoadRequestQueryFilterLogicalOr
    | V1LoadRequestQueryFilterLogicalAnd
)


class V1LoadRequestQueryTimeDimension(BaseModel):
    dimension: str = Field(description="The name of the time dimension.")

    granularity: TimeGranularity | None = Field(
        default=None,
        description="Granularity level for the time dimension. "
        "Setting this to null will filter by the specified time dimension without grouping.",
    )

    date_range: str | list[str] | None = Field(
        default=None,
        alias="dateRange",
        description="An array of dates with the following format YYYY-MM-DD or in YYYY-MM-DDTHH:mm:ss.SSS format. "
        "Values should always be local and in query timezone. Dates in YYYY-MM-DD format are also accepted. "
        "Such dates are padded to the start and end of the day if used in start and end of date range interval accordingly.",
    )


class V1LoadRequestQuery(BaseModel):
    measures: list[str] | None = Field(
        default=None, description="List of measures to be queried."
    )

    dimensions: list[str] | None = Field(
        default=None, description="List of dimensions to be queried."
    )

    segments: list[str] | list[dict[str, Any]] | None = Field(
        default=None,
        description="List of segments to be used in the query. "
        "A segment is a named filter defined in the data model.",
    )

    time_dimensions: list[V1LoadRequestQueryTimeDimension] | None = Field(
        default=None,
        alias="timeDimensions",
        description="List of time dimensions to be used in the query.",
    )

    order: list[list[str] | dict[str, Any]] | None = Field(
        default=None,
        description="Ordering criteria for the query, specified as a dictionary of measures "
        "or dimensions with `asc` or `desc` values.",
    )

    limit: int | None = Field(
        default=None,
        description="Maximum number of rows to return in the query result.",
    )

    offset: int | None = Field(
        default=None,
        description="Number of initial rows to skip in the query result. Default is 0.",
    )

    filters: list[V1LoadRequestQueryFilterItem] | None = Field(
        default=None, description="List of filters to apply to the query."
    )

    timezone: str | None = Field(
        default=None,
        description="Time zone to be used for the query, specified in the TZ Database Name format "
        "(e.g., `America/Los_Angeles`).",
    )

    renew_query: bool | None = Field(
        default=None,
        alias="renewQuery",
        description="Cube will renew all refreshKey for queries and query results in the foreground. "
        "However, if the refreshKey (or refreshKey.every) doesn't indicate that there's a need for an update "
        "this setting has no effect. The default value is false",
    )

    ungrouped: bool | None = Field(
        default=None,
        description="If set to true, Cube will run an ungrouped query.",
    )


class V1LoadResult(BaseModel):
    query: V1LoadRequestQuery | None = Field(
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


# Handle forward references
V1LoadRequestQueryFilterLogicalOr.model_rebuild()
V1LoadRequestQueryFilterLogicalAnd.model_rebuild()
