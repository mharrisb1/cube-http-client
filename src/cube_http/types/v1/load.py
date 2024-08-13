from typing import Any, Dict, List, Literal, Optional, Tuple, TypedDict, Union
from typing_extensions import NotRequired

from pydantic import BaseModel, Field

from ..._utils.recursive import model_build_recursive

from .meta import (
    V1CubeMetaDimension,
    V1CubeMetaMeasure,
    V1CubeMetaSegment,
)


class V1LoadResultAnnotation(BaseModel):
    measures: Dict[str, V1CubeMetaMeasure]
    """Annotations for measures in the result."""

    dimensions: Dict[str, V1CubeMetaDimension]
    """Annotations for dimensions in the result."""

    segments: Dict[str, V1CubeMetaSegment]
    """Annotations for segments in the result."""

    time_dimensions: Dict[str, V1CubeMetaDimension] = Field(
        alias="timeDimensions"
    )
    """Annotations for time dimensions in the result."""


class V1LoadResult(BaseModel):
    query: Optional["V1LoadRequestQuery"] = None
    """The original query object."""

    data: List[Dict[str, Any]]
    """Data returned by the load result."""

    last_refresh_time: Optional[str] = Field(
        alias="lastRefreshTime", default=None
    )
    """Timestamp indicating the last time the query was refreshed."""

    refresh_key_values: Optional[List[List[Dict[str, Any]]]] = Field(
        alias="refreshKeyValues", default=None
    )
    """Values of the refresh key used for the query."""

    used_pre_aggregations: Optional[Dict[str, Any]] = Field(
        alias="usedPreAggregations", default=None
    )
    """Information on pre-aggregations used in the query."""

    transformed_query: Optional[Dict[str, Any]] = Field(
        alias="transformedQuery", default=None
    )
    """The query after being transformed, usually for optimization purposes."""

    request_id: Optional[str] = Field(alias="requestId", default=None)
    """Unique identifier for the request."""

    annotation: V1LoadResultAnnotation
    """Annotations for the load result."""

    data_source: Optional[str] = Field(alias="dataSource", default=None)
    """The data source from which the result was loaded."""

    db_type: Optional[str] = Field(alias="dbType", default=None)
    """The type of database queried."""

    ext_db_type: Optional[str] = Field(alias="exDbType", default=None)
    """External database type, if applicable."""

    external: Optional[bool] = None
    """Indicates if the query result was fetched from an external source."""

    slow_query: Optional[bool] = Field(alias="slowQuery", default=None)
    """Indicates if the query is considered slow."""


class V1LoadResponse(BaseModel):
    pivot_query: Optional["V1LoadRequestQuery"] = Field(
        alias="pivotQuery", default=None
    )
    """The pivot query associated with the load response."""

    query_type: Optional[str] = Field(alias="queryType", default=None)
    """Type of the query, primarily for internal use."""

    slow_query: Optional[bool] = Field(alias="slowQuery", default=None)
    """Indicates if the query was considered slow."""

    results: List[V1LoadResult]
    """List of results obtained from the load response."""


V1LoadRequestQueryFilterOperator = Literal[
    "equals",
    "notEquals",
    "contains",
    "notContains",
    "startsWith",
    "notStartsWith",
    "endsWith",
    "notEndsWith",
    "gt",
    "gte",
    "lt",
    "lte",
    "set",
    "notSet",
    "inDateRange",
    "notInDateRange",
    "beforeDate",
    "afterDate",
    "measureFilter",
]


class V1LoadRequestQueryFilterBase(BaseModel):
    member: Optional[str] = None
    """Dimension or measure to be used in the filter, e.g., `stories.isDraft`. 
    Differentiates between filtering dimensions and filtering measures."""

    operator: Optional[V1LoadRequestQueryFilterOperator] = None
    """Operator to apply in the filter. 
    Some operators are exclusive to measures, while others depend on the dimension type."""

    values: Optional[List[str]] = None
    """List of values for the filter, provided as strings. 
    For dates, use the `YYYY-MM-DD` format."""


class V1LoadRequestQueryFilterLogicalAnd(BaseModel):
    and_: Optional[List["V1LoadRequestQueryFilterItem"]] = Field(
        alias="and", default=None
    )
    """A list of filters or other logical operators to be combined using AND logic."""


class V1LoadRequestQueryFilterLogicalOr(BaseModel):
    or_: Optional[List["V1LoadRequestQueryFilterItem"]] = Field(
        alias="or", default=None
    )
    """A list of filters or other logical operators to be combined using OR logic."""


V1LoadRequestQueryFilterItem = Union[
    V1LoadRequestQueryFilterBase,
    V1LoadRequestQueryFilterLogicalOr,
    V1LoadRequestQueryFilterLogicalAnd,
]

model_build_recursive(V1LoadRequestQueryFilterLogicalAnd)
model_build_recursive(V1LoadRequestQueryFilterLogicalOr)


V1LoadRequestQueryTimeDimensionGranularity = Literal[
    "second",
    "minute",
    "hour",
    "day",
    "week",
    "month",
    "quarter",
    "year",
]


class V1LoadRequestQueryTimeDimension(BaseModel):
    dimension: str
    """The name of the time dimension."""

    granularity: Optional[V1LoadRequestQueryTimeDimensionGranularity] = None
    """Granularity level for the time dimension. 
    Setting this to null will filter by the specified time dimension without grouping."""

    date_range: Optional[Union[str, Tuple[str, str]]] = Field(
        alias="dateRange", default=None
    )
    """Date range for filtering, either as a string in `YYYY-MM-DD` format 
    or as a tuple of strings representing start and end dates."""


V1LoadRequestQueryOrderDirection = Literal["asc", "desc"]

V1LoadRequestQueryOrder = Union[
    Dict[str, V1LoadRequestQueryOrderDirection],
    List[str],
]


class V1LoadRequestQuery(BaseModel):
    measures: Optional[List[str]] = None
    """List of measures to be queried."""

    dimensions: Optional[List[str]] = None
    """List of dimensions to be queried."""

    segments: Optional[List[str]] = None
    """List of segments to be used in the query. 
    A segment is a named filter defined in the data model."""

    time_dimensions: Optional[List[V1LoadRequestQueryTimeDimension]] = Field(
        alias="timeDimensions", default=None
    )
    """List of time dimensions to be used in the query."""

    order: Optional[V1LoadRequestQueryOrder] = None
    """Ordering criteria for the query, specified as a dictionary of measures 
    or dimensions with `asc` or `desc` values."""

    limit: Optional[int] = None
    """Maximum number of rows to return in the query result."""

    offset: Optional[int] = None
    """Number of initial rows to skip in the query result. Default is 0."""

    filters: Optional[List[V1LoadRequestQueryFilterItem]] = None
    """List of filters to apply to the query."""

    timezone: Optional[str] = None
    """Time zone to be used for the query, specified in the TZ Database Name format 
    (e.g., `America/Los_Angeles`)."""

    renew_query: Optional[bool] = Field(alias="renewQuery", default=None)
    """Whether to renew all refresh keys for queries and query results in the foreground. 
    Default is false."""

    total: Optional[bool] = None
    """If true, Cube will run a total query and return the total number of rows, 
    ignoring any row limit or offset. Default is false."""

    ungrouped: Optional[bool] = None
    """Indicates if the query should be ungrouped."""

    query_type: Optional[str] = Field(alias="queryType", default=None)
    """Type of the query, for internal use."""


class V1LoadRequest(BaseModel):
    query_type: Optional[Literal["multi"]] = Field(
        alias="queryType", default=None
    )
    """Specifies the type of the query."""

    query: Optional[Union[V1LoadRequestQuery, List[V1LoadRequestQuery]]] = None
    """The query or a list of queries to execute."""


#############
# TypedDicts
#############


class V1LoadRequestQueryFilterBaseDict(TypedDict):
    member: NotRequired[str]
    """Dimension or measure to be used in the filter, e.g., `stories.isDraft`. 
    Differentiates between filtering dimensions and filtering measures."""

    operator: NotRequired[V1LoadRequestQueryFilterOperator]
    """Operator to apply in the filter. 
    Some operators are exclusive to measures, while others depend on the dimension type."""

    values: NotRequired[List[str]]
    """List of values for the filter, provided as strings. 
    For dates, use the `YYYY-MM-DD` format."""


V1LoadRequestQueryFilterLogicalAndDict = TypedDict(
    "V1LoadRequestQueryFilterLogicalAndDict",
    {
        "and": NotRequired[List["V1LoadRequestQueryFilterItemDict"]],
    },
)


V1LoadRequestQueryFilterLogicalOrDict = TypedDict(
    "V1LoadRequestQueryFilterLogicalOrDict",
    {
        "or": NotRequired[List["V1LoadRequestQueryFilterItemDict"]],
    },
)

V1LoadRequestQueryFilterItemDict = Union[
    V1LoadRequestQueryFilterBaseDict,
    V1LoadRequestQueryFilterLogicalOrDict,
    V1LoadRequestQueryFilterLogicalAndDict,
]


class V1LoadRequestQueryTimeDimensionDict(TypedDict):
    dimension: str
    """The name of the time dimension."""

    granularity: NotRequired[V1LoadRequestQueryTimeDimensionGranularity]
    """Granularity level for the time dimension. 
    Setting this to null will filter by the specified time dimension without grouping."""

    dateRange: NotRequired[Union[str, Tuple[str, str]]]
    """Date range for filtering, either as a string in `YYYY-MM-DD` format 
    or as a tuple of strings representing start and end dates."""


V1LoadRequestQueryOrderDict = Union[
    dict[str, V1LoadRequestQueryOrderDirection],
    List[str],
]


class V1LoadRequestQueryDict(TypedDict):
    measures: NotRequired[List[str]]
    """List of measures to be queried."""

    dimensions: NotRequired[List[str]]
    """List of dimensions to be queried."""

    segments: NotRequired[List[str]]
    """List of segments to be used in the query. 
    A segment is a named filter defined in the data model."""

    timeDimensions: NotRequired[List[V1LoadRequestQueryTimeDimensionDict]]
    """List of time dimensions to be used in the query."""

    order: NotRequired[V1LoadRequestQueryOrderDict]
    """Ordering criteria for the query, specified as a dictionary of measures 
    or dimensions with `asc` or `desc` values."""

    limit: NotRequired[int]
    """Maximum number of rows to return in the query result."""

    offset: NotRequired[int]
    """Number of initial rows to skip in the query result. Default is 0."""

    filters: NotRequired[List[V1LoadRequestQueryFilterItemDict]]
    """List of filters to apply to the query."""

    timezone: NotRequired[str]
    """Time zone to be used for the query, specified in the TZ Database Name format 
    (e.g., `America/Los_Angeles`)."""

    renewQuery: NotRequired[bool]
    """Whether to renew all refresh keys for queries and query results in the foreground. 
    Default is false."""

    total: NotRequired[bool]
    """If true, Cube will run a total query and return the total number of rows, 
    ignoring any row limit or offset. Default is false."""

    ungrouped: NotRequired[bool]
    """Indicates if the query should be ungrouped."""

    queryType: NotRequired[str]
    """Type of the query, for internal use."""
