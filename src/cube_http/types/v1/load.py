from typing import Any, Dict, List, Optional, TypedDict, Union
from typing_extensions import NotRequired

from pydantic import BaseModel, Field


class V1LoadResultAnnotation(BaseModel):
    measures: Dict[str, Any] = Field(description="Annotations for measures")
    dimensions: Dict[str, Any] = Field(description="Annotations for dimensions")
    segments: Dict[str, Any] = Field(description="Annotations for segments")
    time_dimensions: Dict[str, Any] = Field(
        alias="timeDimensions", description="Annotations for time dimensions"
    )


class V1LoadResult(BaseModel):
    data_source: Optional[str] = Field(
        alias="dataSource",
        default=None,
        description="Data source of the load result",
    )
    annotation: V1LoadResultAnnotation = Field(
        description="Annotations for the load result"
    )
    data: List[Dict[str, str]] = Field(description="Data of the load result")


class V1LoadResponse(BaseModel):
    pivot_query: Optional[Dict[str, Any]] = Field(
        alias="pivotQuery",
        default=None,
        description="Pivot query of the load response",
    )
    slow_query: Optional[bool] = Field(
        alias="slowQuery",
        default=None,
        description="Indicates if the query is slow",
    )
    query_type: Optional[str] = Field(
        alias="queryType", default=None, description="Type of the query"
    )
    results: List[V1LoadResult] = Field(
        description="Results of the load response"
    )


class V1LoadRequestQueryFilterLogicalAnd(BaseModel):
    and_: Optional[List[Dict[str, Any]]] = Field(
        default=None, alias="and", description="AND filter logic"
    )


class V1LoadRequestQueryFilterLogicalOr(BaseModel):
    or_: Optional[List[Dict[str, Any]]] = Field(
        default=None, alias="or", description="OR filter logic"
    )


class V1LoadRequestQueryFilterBase(BaseModel):
    member: Optional[str] = Field(default=None, description="Member to filter")
    operator: Optional[str] = Field(default=None, description="Filter operator")
    values: Optional[List[str]] = Field(
        default=None, description="Values for the filter"
    )


class V1LoadRequestQueryTimeDimension(BaseModel):
    dimension: str = Field(description="Time dimension to query")
    granularity: Optional[str] = Field(
        default=None, description="Granularity of the time dimension"
    )
    date_range: Optional[Union[str, List[str]]] = Field(
        alias="dateRange",
        default=None,
        description="Date range for the time dimension",
    )


try:
    from pydantic import RootModel

    V1LoadRequestQueryFilterItem = RootModel[  # type: ignore
        Union[
            V1LoadRequestQueryFilterBase,
            V1LoadRequestQueryFilterLogicalOr,
            V1LoadRequestQueryFilterLogicalAnd,
        ]
    ]

except ImportError:

    class V1LoadRequestQueryFilterItem(BaseModel):  # type: ignore
        __root__: Union[
            V1LoadRequestQueryFilterBase,
            V1LoadRequestQueryFilterLogicalOr,
            V1LoadRequestQueryFilterLogicalAnd,
        ]


class V1LoadRequestQuery(BaseModel):
    measures: Optional[List[str]] = Field(
        default=None, description="List of measures to query"
    )
    dimensions: Optional[List[str]] = Field(
        default=None, description="List of dimensions to query"
    )
    segments: Optional[List[str]] = Field(
        default=None, description="List of segments to query"
    )
    time_dimensions: Optional[List[V1LoadRequestQueryTimeDimension]] = Field(
        alias="timeDimensions",
        default=None,
        description="List of time dimensions to query",
    )
    order: Optional[List[List[str]]] = Field(
        default=None, description="Order of the query result"
    )
    limit: Optional[int] = Field(
        default=None, description="Limit for the query result"
    )
    offset: Optional[int] = Field(
        default=None, description="Offset for the query result"
    )
    filters: Optional[List[V1LoadRequestQueryFilterItem]] = Field(
        default=None, description="Filters for the query"
    )
    ungrouped: Optional[bool] = Field(
        default=None, description="Indicates if the query is ungrouped"
    )


class V1LoadRequest(BaseModel):
    query_type: Optional[str] = Field(
        alias="queryType", default=None, description="Type of the query"
    )
    query: Optional[Union[V1LoadRequestQuery, List[V1LoadRequestQuery]]] = Field(
        default=None, description="Query or list of queries"
    )


#############
# TypedDicts
#############


V1LoadRequestQueryFilterLogicalAndDict = TypedDict(
    "V1LoadRequestQueryFilterLogicalAndDict",
    {
        "and": NotRequired[List[Dict[str, Any]]],
    },
)


V1LoadRequestQueryFilterLogicalOrDict = TypedDict(
    "V1LoadRequestQueryFilterLogicalOrDict",
    {
        "or": NotRequired[List[Dict[str, Any]]],
    },
)


class V1LoadRequestQueryFilterBaseDict(TypedDict):
    member: NotRequired[str]
    operator: NotRequired[str]
    values: NotRequired[List[str]]


class V1LoadRequestQueryTimeDimensionDict(TypedDict):
    dimension: str
    granularity: NotRequired[str]
    dateRange: NotRequired[Union[str, List[str]]]


V1LoadRequestQueryFilterItemDict = Union[
    V1LoadRequestQueryFilterBaseDict,
    V1LoadRequestQueryFilterLogicalOrDict,
    V1LoadRequestQueryFilterLogicalAndDict,
]


class V1LoadRequestQueryDict(TypedDict):
    measures: NotRequired[List[str]]
    dimensions: NotRequired[List[str]]
    segments: NotRequired[List[str]]
    timeDimensions: NotRequired[List[V1LoadRequestQueryTimeDimensionDict]]
    order: NotRequired[List[List[str]]]
    limit: NotRequired[int]
    offset: NotRequired[int]
    filters: NotRequired[List[V1LoadRequestQueryFilterItemDict]]
    ungrouped: NotRequired[bool]
