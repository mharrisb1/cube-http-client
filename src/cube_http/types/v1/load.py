from typing import Any, Dict, List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired

from pydantic import BaseModel, Field

from .._base import RequestModel, ResponseModel
from ..._utils.serde import model_parse


class V1LoadResultAnnotation(BaseModel):
    measures: Dict[str, Dict[str, Any]] = Field(
        description="Annotations for measures in the result."
    )

    dimensions: Dict[str, Dict[str, Any]] = Field(
        description="Annotations for dimensions in the result."
    )

    segments: Dict[str, Dict[str, Any]] = Field(
        description="Annotations for segments in the result."
    )

    time_dimensions: Dict[str, Dict[str, Any]] = Field(
        alias="timeDimensions",
        description="Annotations for time dimensions in the result.",
    )


class V1LoadResult(BaseModel):
    query: Optional[Dict[str, Any]] = Field(
        default=None, description="The original query object."
    )

    data: List[Dict[str, Any]] = Field(
        description="Data returned by the load result."
    )

    last_refresh_time: Optional[str] = Field(
        alias="lastRefreshTime",
        default=None,
        description="Timestamp indicating the last time the query was refreshed.",
    )

    refresh_key_values: Optional[List[List[Dict[str, Any]]]] = Field(
        alias="refreshKeyValues",
        default=None,
        description="Values of the refresh key used for the query.",
    )

    used_pre_aggregations: Optional[Dict[str, Any]] = Field(
        alias="usedPreAggregations",
        default=None,
        description="Information on pre-aggregations used in the query.",
    )

    transformed_query: Optional[Dict[str, Any]] = Field(
        alias="transformedQuery",
        default=None,
        description="The query after being transformed, usually for optimization purposes.",
    )

    request_id: Optional[str] = Field(
        alias="requestId",
        default=None,
        description="Unique identifier for the request.",
    )

    annotation: V1LoadResultAnnotation = Field(
        description="Annotations for the load result."
    )

    data_source: Optional[str] = Field(
        alias="dataSource",
        default=None,
        description="The data source from which the result was loaded.",
    )

    db_type: Optional[str] = Field(
        alias="dbType", default=None, description="The type of database queried."
    )

    ext_db_type: Optional[str] = Field(
        alias="exDbType",
        default=None,
        description="External database type, if applicable.",
    )

    external: Optional[bool] = Field(
        default=None,
        description="Indicates if the query result was fetched from an external source.",
    )

    slow_query: Optional[bool] = Field(
        alias="slowQuery",
        default=None,
        description="Indicates if the query is considered slow.",
    )


class V1LoadResponse(ResponseModel):
    pivot_query: Optional[Dict[str, Any]] = Field(
        alias="pivotQuery",
        default=None,
        description="The pivot query associated with the load response.",
    )

    query_type: Optional[str] = Field(
        alias="queryType",
        default=None,
        description="Type of the query, primarily for internal use.",
    )

    slow_query: Optional[bool] = Field(
        alias="slowQuery",
        default=None,
        description="Indicates if the query was considered slow.",
    )

    results: List[V1LoadResult] = Field(
        description="List of results obtained from the load response."
    )


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


class V1LoadRequestQueryFilterItem(BaseModel):
    member: Optional[str] = None
    """Dimension or measure to be used in the filter, e.g., `stories.isDraft`. 
    Differentiates between filtering dimensions and filtering measures."""

    operator: Optional[V1LoadRequestQueryFilterOperator] = None
    """Operator to apply in the filter. 
    Some operators are exclusive to measures, while others depend on the dimension type."""

    values: Optional[List[str]] = None
    """List of values for the filter, provided as strings. 
    For dates, use the `YYYY-MM-DD` format."""

    and_: Optional[List["V1LoadRequestQueryFilterItem"]] = Field(
        alias="and", default=None
    )
    """A list of filters or other logical operators to be combined using AND logic."""

    or_: Optional[List["V1LoadRequestQueryFilterItem"]] = Field(
        alias="or", default=None
    )
    """A list of filters or other logical operators to be combined using OR logic."""

    # TODO(mh): add validator to not allow user to set base filter fields and logical filters


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
    dimension: str = Field(description="The name of the time dimension.")

    granularity: Optional[V1LoadRequestQueryTimeDimensionGranularity] = Field(
        default=None,
        description="Granularity level for the time dimension. Setting this to null will filter by the specified time dimension without grouping.",
    )

    date_range: Optional[Union[str, List[str]]] = Field(
        alias="dateRange",
        default=None,
        description="An array of dates with the following format YYYY-MM-DD or in YYYY-MM-DDTHH:mm:ss.SSS format. Values should always be local and in query timezone. Dates in YYYY-MM-DD format are also accepted. Such dates are padded to the start and end of the day if used in start and end of date range interval accordingly. Please note that for timestamp comparison, >= and <= operators are used. It requires, for example, that the end date range date 2020-01-01 is padded to 2020-01-01T23:59:59.999. If only one date is specified it's equivalent to passing two of the same dates as a date range. You can also pass a string with a relative date range, for example, `today`, `yesterday`, `tomorrow`, `last year`, `last quarter`, `last 360 days`, `next month`, `last 6 month`, `from 7 days ago to now`, `from now to 2 weeks from now`.",
    )


class V1LoadRequestQuery(BaseModel):
    measures: Optional[List[str]] = Field(
        default=None, description="List of measures to be queried."
    )

    dimensions: Optional[List[str]] = Field(
        default=None, description="List of dimensions to be queried."
    )

    segments: Optional[List[str]] = Field(
        default=None,
        description="List of segments to be used in the query. A segment is a named filter defined in the data model.",
    )

    time_dimensions: Optional[List[V1LoadRequestQueryTimeDimension]] = Field(
        alias="timeDimensions",
        default=None,
        description="List of time dimensions to be used in the query.",
    )

    order: Optional[List[List[str]]] = Field(
        default=None,
        description="Ordering criteria for the query, specified as a dictionary of measures or dimensions with `asc` or `desc` values.",
    )

    limit: Optional[int] = Field(
        default=None,
        description="Maximum number of rows to return in the query result.",
    )

    offset: Optional[int] = Field(
        default=None,
        description="Number of initial rows to skip in the query result. Default is 0.",
    )

    filters: Optional[List[V1LoadRequestQueryFilterItem]] = Field(
        default=None, description="List of filters to apply to the query."
    )

    timezone: Optional[str] = Field(
        default=None,
        description="Time zone to be used for the query, specified in the TZ Database Name format (e.g., `America/Los_Angeles`).",
    )

    renew_query: Optional[bool] = Field(
        alias="renewQuery",
        default=None,
        description="Cube will renew all refreshKey for queries and query results in the foreground. However, if the refreshKey (or refreshKey.every) doesn't indicate that there's a need for an update this setting has no effect. The default value is false",
    )

    ungrouped: Optional[bool] = Field(
        default=None,
        description="If set to true, Cube will run an ungrouped query.",
    )


class V1LoadRequest(RequestModel):
    query_type: Optional[Literal["multi"]] = Field(
        alias="queryType",
        default=None,
        description="Specifies the type of the query.",
    )

    query: Optional[V1LoadRequestQuery] = Field(
        default=None, description="The query or a list of queries to execute."
    )

    @classmethod
    def build(cls, query: "V1LoadRequestQueryDict") -> "V1LoadRequest":
        return cls(
            queryType="multi",
            query=model_parse(V1LoadRequestQuery, query),
        )


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

    dateRange: NotRequired[Union[str, List[str]]]
    """An array of dates with the following format YYYY-MM-DD or in YYYY-MM-DDTHH:mm:ss.SSS format. 
    Values should always be local and in query timezone. Dates in YYYY-MM-DD format are also accepted. 
    Such dates are padded to the start and end of the day if used in start and end of date range interval accordingly. 
    Please note that for timestamp comparison, >= and <= operators are used. 
    It requires, for example, that the end date range date 2020-01-01 is padded to 2020-01-01T23:59:59.999. 
    If only one date is specified it's equivalent to passing two of the same dates as a date range. 
    You can also pass a string with a relative date range, for example, `today`, `yesterday`, `tomorrow`, `last year`, 
    `last quarter`, `last 360 days`, `next month`, `last 6 month`, `from 7 days ago to now`, `from now to 2 weeks from now`."""


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

    order: NotRequired[List[List[str]]]
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
    """Cube will renew all refreshKey for queries and query results in the foreground. However, if the refreshKey (or refreshKey.every) doesn't indicate that there's a need for an update this setting has no effect. The default value is false"""

    ungrouped: NotRequired[bool]
    """If set to true, Cube will run an ungrouped query."""
