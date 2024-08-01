from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class V1CubeMetaJoin(BaseModel):
    name: str
    relationship: str
    sql: Optional[str] = Field(
        default=None, description="SQL for join condition"
    )


class V1CubeMetaSegment(BaseModel):
    name: str
    title: str
    short_title: Optional[str] = Field(
        alias="shortTitle",
        default=None,
        description="Short title of the segment",
    )
    sql: Optional[str] = Field(
        default=None, description="SQL for segment condition"
    )


class V1CubeMetaDimension(BaseModel):
    name: str
    type: str
    title: Optional[str] = Field(
        default=None, description="Title of the dimension"
    )
    short_title: Optional[str] = Field(
        alias="shortTitle",
        default=None,
        description="Short title of the dimension",
    )
    description: Optional[str] = Field(
        default=None, description="Description of the dimension"
    )
    format: Optional[str] = Field(
        default=None, description="Format of the dimension"
    )
    sql: Optional[str] = Field(default=None, description="SQL for the dimension")
    primary_key: Optional[bool] = Field(
        alias="primaryKey",
        default=None,
        description="If the dimension is a primary key",
    )
    public: Optional[bool] = Field(
        default=None, description="If the dimension is public"
    )
    is_visible: Optional[bool] = Field(
        alias="isVisible",
        default=None,
        description="Visibility of the dimension",
    )
    suggest_filter_values: Optional[bool] = Field(
        alias="suggestFilterValues",
        default=None,
        description="Suggest filter values for the dimension",
    )


class V1CubeMetaMeasure(BaseModel):
    name: str
    type: str
    title: Optional[str] = Field(
        default=None, description="Title of the measure"
    )
    short_title: Optional[str] = Field(
        alias="shortTitle",
        default=None,
        description="Short title of the measure",
    )
    description: Optional[str] = Field(
        default=None, description="Description of the measure"
    )
    sql: Optional[str] = Field(default=None, description="SQL for the measure")
    agg_type: Optional[str] = Field(
        alias="aggType",
        default=None,
        description="Aggregation type of the measure",
    )
    public: Optional[bool] = Field(
        default=None, description="If the measure is public"
    )
    is_visible: Optional[bool] = Field(
        alias="isVisible", default=None, description="Visibility of the measure"
    )
    cumulative: Optional[bool] = Field(
        default=None, description="If the measure is cumulative"
    )
    cumulative_total: Optional[bool] = Field(
        alias="cumulativeTotal",
        default=None,
        description="If the measure is cumulative total",
    )
    drill_members: Optional[List[str]] = Field(
        alias="drillMembers",
        default=None,
        description="Drill members for the measure",
    )
    drill_members_grouped: Optional[Dict[str, List[str]]] = Field(
        alias="drillMembersGrouped",
        default=None,
        description="Grouped drill members for the measure",
    )


class V1CubeMeta(BaseModel):
    name: str
    title: Optional[str] = Field(default=None, description="Title of the cube")
    description: Optional[str] = Field(
        default=None, description="Description of the cube"
    )
    file_name: Optional[str] = Field(
        alias="fileName", default=None, description="File name of the cube"
    )
    public: Optional[bool] = Field(
        default=None, description="If the cube is public"
    )
    is_visible: Optional[bool] = Field(
        alias="isVisible", default=None, description="Visibility of the cube"
    )
    sql: Optional[str] = Field(
        default=None, description="SQL query for the cube"
    )
    measures: List[V1CubeMetaMeasure]
    dimensions: List[V1CubeMetaDimension]
    segments: List[V1CubeMetaSegment]
    joins: Optional[List[V1CubeMetaJoin]] = Field(
        default=None, description="Joins for the cube"
    )
    pre_aggregations: Optional[List[Any]] = Field(
        alias="preAggregations",
        default=None,
        description="Pre-aggregations for the cube",
    )
    meta: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadata of the cube"
    )
    connected_component: Optional[int] = Field(
        alias="connectedComponent",
        default=None,
        description="Connected component of the cube",
    )


class V1MetaResponse(BaseModel):
    cubes: Optional[List[V1CubeMeta]] = Field(
        default=None, description="List of cube metadata"
    )
