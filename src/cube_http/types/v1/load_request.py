from typing import TypedDict, Union
from typing_extensions import NotRequired, Required

from .operators import FilterOperator
from .time_granularities import TimeGranularity


class V1LoadRequestQueryFilterBase(TypedDict):
    member: NotRequired[str]
    """Dimension or measure to be used in the filter, e.g., `stories.isDraft`. 
    Differentiates between filtering dimensions and filtering measures."""

    operator: NotRequired[FilterOperator]
    """Operator to apply in the filter. 
    Some operators are exclusive to measures, while others depend on the dimension type."""

    values: NotRequired[list[str]]
    """List of values for the filter, provided as strings. 
    For dates, use the `YYYY-MM-DD` format."""


V1LoadRequestQueryFilterLogicalAnd = TypedDict(
    "V1LoadRequestQueryFilterLogicalAnd",
    {
        "and": NotRequired[list["V1LoadRequestQueryFilterItem"]],
    },
)


V1LoadRequestQueryFilterLogicalOr = TypedDict(
    "V1LoadRequestQueryFilterLogicalOr",
    {
        "or": NotRequired[list["V1LoadRequestQueryFilterItem"]],
    },
)

V1LoadRequestQueryFilterItem = Union[
    V1LoadRequestQueryFilterBase,
    V1LoadRequestQueryFilterLogicalOr,
    V1LoadRequestQueryFilterLogicalAnd,
]


class V1LoadRequestQueryTimeDimension(TypedDict):
    dimension: str
    """The name of the time dimension."""

    granularity: NotRequired[TimeGranularity]
    """Granularity level for the time dimension. 
    Setting this to null will filter by the specified time dimension without grouping."""

    dateRange: NotRequired[Union[str, list[str]]]
    """An array of dates with the following format YYYY-MM-DD or in YYYY-MM-DDTHH:mm:ss.SSS format. 
    Values should always be local and in query timezone. Dates in YYYY-MM-DD format are also accepted. 
    Such dates are padded to the start and end of the day if used in start and end of date range interval accordingly. 
    Please note that for timestamp comparison, >= and <= operators are used. 
    It requires, for example, that the end date range date 2020-01-01 is padded to 2020-01-01T23:59:59.999. 
    If only one date is specified it's equivalent to passing two of the same dates as a date range. 
    You can also pass a string with a relative date range, for example, `today`, `yesterday`, `tomorrow`, `last year`, 
    `last quarter`, `last 360 days`, `next month`, `last 6 month`, `from 7 days ago to now`, `from now to 2 weeks from now`."""


class V1LoadRequestQuery(TypedDict):
    measures: NotRequired[list[str]]
    """List of measures to be queried."""

    dimensions: NotRequired[list[str]]
    """List of dimensions to be queried."""

    segments: NotRequired[list[str]]
    """List of segments to be used in the query. 
    A segment is a named filter defined in the data model."""

    timeDimensions: NotRequired[list[V1LoadRequestQueryTimeDimension]]
    """List of time dimensions to be used in the query."""

    order: NotRequired[list[list[str]] | list[dict[str, str]]]
    """Ordering criteria for the query, specified as a dictionary of measures 
    or dimensions with `asc` or `desc` values."""

    limit: NotRequired[int]
    """Maximum number of rows to return in the query result."""

    offset: NotRequired[int]
    """Number of initial rows to skip in the query result. Default is 0."""

    filters: NotRequired[list[V1LoadRequestQueryFilterItem]]
    """List of filters to apply to the query."""

    timezone: NotRequired[str]
    """Time zone to be used for the query, specified in the TZ Database Name format 
    (e.g., `America/Los_Angeles`)."""

    renewQuery: NotRequired[bool]
    """Cube will renew all refreshKey for queries and query results in the foreground. However, if the refreshKey (or refreshKey.every) doesn't indicate that there's a need for an update this setting has no effect. The default value is false"""

    ungrouped: NotRequired[bool]
    """If set to true, Cube will run an ungrouped query."""


class V1LoadRequest(TypedDict):
    query: Required[V1LoadRequestQuery]
    """A single URL encoded Cube Query"""
