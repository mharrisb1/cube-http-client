from typing import Any, Literal

from pydantic import BaseModel, Field

from .._base import ResponseModel


class V1CubeMetaJoin(BaseModel):
    name: str = Field(
        description="The name of the joined cube. It must match the name of the cube being joined and follow the naming conventions."
    )

    relationship: Literal[
        "one_to_one",
        "one_to_many",
        "many_to_one",
        "has_one",
        "has_many",
        "belongs_to",
        "hasOne",
        "hasMany",
        "belongsTo",
    ] = Field(
        description="The type of relationship between the cubes. Valid relationships are `one_to_one`, `one_to_many`, and `many_to_one`."
    )

    sql: str | None = Field(
        default=None,
        description="The SQL ON clause that specifies the join condition between the cubes. It is important to accurately define the matching columns to ensure correct join behavior.",
    )


class V1CubeMetaSegment(BaseModel):
    name: str = Field(
        default="",
        description="The unique identifier for the segment. It must be unique among all segments, dimensions, and measures within a cube and follow naming conventions.",
    )

    title: str | None = Field(
        default=None,
        description="A human-readable display name for the segment. By default, Cube will humanize the segment's title, but you can use this parameter to customize it.",
    )

    short_title: str | None = Field(
        default=None,
        alias="shortTitle",
        description="A short human-readable name for the segment. This can be used in places where a shorter label is needed.",
    )

    description: str | None = Field(
        default=None,
        description="A description providing more context about what the segment represents. This is useful for ensuring that users understand the attribute correctly.",
    )

    sql: str | None = Field(
        default=None,
        description="A required parameter that defines the SQL expression used to filter the data for this segment. The SQL should be valid within a WHERE clause and can implement complex filtering logic.",
    )

    public: bool | None = Field(
        default=None,
        description="Controls the visibility of the segment. When set to `False`, the segment cannot be queried through the API. Defaults to `True`.",
    )


class V1CubeMetaDimensionLinkFormat(BaseModel):
    type: Literal["link"] = Field(
        description="Format link type. Will always be `link`"
    )

    label: str = Field(description="Link label")


V1CubeMetaDimensionFormat = (
    Literal["imageUrl", "id", "link", "currency", "percent", "number"]
    | V1CubeMetaDimensionLinkFormat
)


class V1CubeMetaDimension(BaseModel):
    name: str = Field(
        description="The unique identifier for the dimension. It must be unique among all dimensions, measures, and segments within a cube and follow naming conventions.",
    )

    title: str | None = Field(
        default=None,
        description="A human-readable display name for the dimension. By default, Cube will humanize the dimension's name, but you can use this parameter to customize it.",
    )

    short_title: str | None = Field(
        alias="shortTitle",
        default=None,
        description="A short human-readable name for the dimension. This can be used in places where a shorter label is needed.",
    )

    description: str | None = Field(
        default=None,
        description="A description providing more context about what the dimension represents. This is useful for ensuring that users understand the attribute correctly.",
    )

    sql: str | None = Field(
        default=None,
        description="A required parameter that defines the SQL expression used to derive the dimension's value. The SQL should return a value consistent with the dimension's type.",
    )

    type: Literal["time", "string", "number", "boolean", "geo"] = Field(
        description="A required parameter that specifies the type of data the dimension represents."
    )

    format: V1CubeMetaDimensionFormat | None = Field(
        default=None,
        description="Optional parameter to define how the dimension's output should be formatted. Supported formats include `imageUrl`, `id`, `link`, `currency`, and `percent`.",
    )

    case: dict[str, Any] | None = Field(
        default=None,
        description="Optional parameter to define the dimension based on SQL conditions using a case statement. It allows for conditionally assigning labels based on the SQL conditions.",
    )

    meta: dict[str, Any] | None = Field(
        default=None,
        description="Custom metadata associated with the dimension, which can be used to pass additional information to the frontend.",
    )

    primary_key: bool | None = Field(
        alias="primaryKey",
        default=None,
        description="Specifies if the dimension is the primary key for the cube. Setting this to `True` will change the default value of the `public` parameter to `False`.",
    )

    propagate_filters_to_sub_query: bool | None = Field(
        alias="propagateFiltersToSubQuery",
        default=None,
        description="When set to `True`, the filters applied to the query will be passed to the subquery.",
    )

    public: bool | None = Field(
        default=None,
        description="Controls the visibility of the dimension. When set to `False`, the dimension cannot be queried through the API. Defaults to `True`.",
    )

    sub_query: bool | None = Field(
        alias="subQuery",
        default=None,
        description="Enables referencing a measure in a dimension by setting this to `True`. This is an advanced concept that allows for more complex dimension definitions.",
    )


class V1CubeMetaMeasure(BaseModel):
    name: str = Field(
        description="The unique identifier for the measure. It must be unique among all measures, dimensions, and segments within a cube and must follow naming conventions.",
    )

    title: str | None = Field(
        default=None,
        description="A human-readable display name for the measure. By default, Cube will humanize the measure's name, but you can use this parameter to customize it.",
    )

    short_title: str | None = Field(
        alias="shortTitle",
        default=None,
        description="A short human-readable name for the dimension. This can be used in places where a shorter label is needed.",
    )

    description: str | None = Field(
        default=None,
        description="A description providing more context about what the measure represents. This is useful for ensuring that users understand the metric correctly.",
    )

    sql: str | None = Field(
        default=None,
        description="A required parameter that defines the SQL expression used to calculate the measure. Depending on the measure type, this can be an aggregation, a simple SQL expression, or even a calculation involving other measures.",
    )

    type: Literal[
        "string",
        "time",
        "boolean",
        "number",
        "count",
        "count_distinct",
        "count_distinct_approx",
        "sum",
        "avg",
        "min",
        "max",
    ] = Field(
        description="A required parameter that specifies the type of aggregation or calculation the measure represents."
    )

    format: Literal["percent", "currency", "number"] | None = Field(
        default=None,
        description="Defines how the measure's output should be formatted.",
    )

    filters: list[dict[str, Any]] | None = Field(
        default=None,
        description="Optional parameter for defining conditions that must be met for the measure's calculation. This is specified as an array of SQL conditions that are applied to the measure.",
    )

    drill_members: list[str] | None = Field(
        alias="drillMembers",
        default=None,
        description="An array of dimensions that can be used to drill down into the measure. These dimensions provide additional detail when exploring the measure's value.",
    )

    public: bool | None = Field(
        default=None,
        description="Controls the visibility of the measure. When set to `False`, the measure cannot be queried through the API. Defaults to `True`.",
    )

    cumulative: bool | None = Field(
        default=None,
        description="Indicates whether the measure is cumulative, meaning it accumulates values over time.",
    )

    cumulative_total: bool | None = Field(
        alias="cumulativeTotal",
        default=None,
        description="Indicates whether the measure represents a cumulative total.",
    )

    rolling_window: dict[str, str | int] | None = Field(
        alias="rollingWindow",
        default=None,
        description="Defines a rolling window for the measure, allowing the calculation of metrics within a specified time window. The window can be defined with trailing and leading parameters, and it only works with a single time dimension with a defined date range.",
    )

    meta: dict[str, Any] | None = Field(
        default=None,
        description="Custom metadata associated with the measure, which can be used to pass additional information to the frontend.",
    )


class V1CubeMeta(BaseModel):
    name: str = Field(
        description="The unique identifier for the cube. Must be unique among all cubes and views within a deployment and follow the naming conventions."
    )

    title: str | None = Field(
        default=None,
        description="A human-readable display name for the cube. By default, Cube will humanize the cube's name (e.g., `users_orders` becomes `Users Orders`). Use this parameter to customize the display name if the default isn't suitable.",
    )

    description: str | None = Field(
        default=None,
        description="A brief description of the cube to help your team understand its purpose and contents. Useful for ensuring that the data is interpreted correctly by users.",
    )

    file_name: str | None = Field(
        alias="fileName",
        default=None,
        description="The file name associated with the cube definition.",
    )

    sql_table: str | None = Field(
        alias="sqlTable",
        default=None,
        description="Specifies the table in the database that this cube will query. It is a concise alternative to the `sql` parameter when querying entire tables.",
    )

    sql: str | None = Field(
        default=None,
        description="The SQL query that generates the table to be queried by the cube. Typically takes the form of a `SELECT * FROM table` query. For simple table queries, prefer using the `sql_table` parameter.",
    )

    sql_alias: str | None = Field(
        alias="sqlAlias",
        default=None,
        description="Custom SQL alias for the cube. Useful when the auto-generated alias is too long and may be truncated by the database.",
    )

    data_source: str | None = Field(
        alias="dataSource",
        default=None,
        description="Specifies the data source name for the cube. This is useful when data should be fetched from multiple databases. The value is passed to the `driverFactory()` function as part of the context.",
    )

    public: bool | None = Field(
        default=None,
        description="Controls the visibility of the cube. When set to `False`, the cube cannot be queried through the API. Defaults to `True`.",
    )

    is_visible: bool | None = Field(
        alias="isVisible",
        default=None,
        description="Determines if the cube should be visible in the UI. If set to `False`, it will be hidden from the user interface.",
    )

    meta: dict[str, Any] | None = Field(
        default=None,
        description="Custom metadata for the cube. Can be used to pass additional information to the frontend.",
    )

    refresh_key: dict[str, str | dict[str, str]] | None = Field(
        alias="refreshKey",
        default=None,
        description="Defines the refresh key for the cube, used by Cube's caching layer to determine when the data should be refreshed. Can be specified using SQL or an interval (e.g., `every: '1 hour'`).",
    )

    extends: str | None = Field(
        default=None,
        description="Allows extending another cube to reuse its declared members, such as `sql` or `measures`. Useful for creating variations of existing cubes without redefining all properties.",
    )

    measures: list["V1CubeMetaMeasure"] = Field(
        description="List of measures defined within the cube. Measures represent aggregated data points such as counts, sums, or averages."
    )

    dimensions: list["V1CubeMetaDimension"] = Field(
        description="List of dimensions defined within the cube. Dimensions represent categorical data such as dates, strings, or numbers."
    )

    segments: list["V1CubeMetaSegment"] = Field(
        description="List of segments defined within the cube. Segments represent predefined filters on the data, such as 'Active Users'."
    )

    joins: list["V1CubeMetaJoin"] | None = Field(
        default=None,
        description="List of joins between this cube and other cubes. Joins define relationships between cubes, allowing for complex data retrievals.",
    )

    pre_aggregations: list[Any] | None = Field(
        alias="preAggregations",
        default=None,
        description="List of pre-aggregations defined for the cube. Pre-aggregations are used to speed up query performance by storing pre-computed results.",
    )

    connected_component: int | None = Field(
        alias="connectedComponent",
        default=None,
        description="ID of the connected component associated with the cube. This is used internally for query planning and optimization.",
    )


class V1MetaResponse(ResponseModel):
    cubes: list[V1CubeMeta] | None = Field(
        default=None, description="List of cube metadata in the response."
    )
