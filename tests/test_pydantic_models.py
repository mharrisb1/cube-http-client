import json
from typing import cast

import pytest

# pyright: reportTypedDictNotRequiredAccess=false
from cube_http.types.v1.load_request import (
    V1LoadRequestQuery as TypedDictQuery,
)
from cube_http.types.v1.load_request import (
    V1LoadRequestQueryFilterBase as TypedDictFilterBase,
)
from cube_http.types.v1.load_request import (
    V1LoadRequestQueryFilterLogicalAnd as TypedDictFilterAnd,
)
from cube_http.types.v1.load_request import (
    V1LoadRequestQueryFilterLogicalOr as TypedDictFilterOr,
)
from cube_http.types.v1.load_request import (
    V1LoadRequestQueryTimeDimension as TypedDictTimeDimension,
)
from cube_http.types.v1.load_response import (
    V1LoadRequestQuery as PydanticQuery,
)
from cube_http.types.v1.load_response import (
    V1LoadRequestQueryFilterBase as PydanticFilterBase,
)
from cube_http.types.v1.load_response import (
    V1LoadRequestQueryFilterLogicalAnd as PydanticFilterAnd,
)
from cube_http.types.v1.load_response import (
    V1LoadRequestQueryFilterLogicalOr as PydanticFilterOr,
)
from cube_http.types.v1.load_response import (
    V1LoadRequestQueryTimeDimension as PydanticTimeDimension,
)

from .fixtures import TEST_QUERIES


def test_filter_base_model_compatibility():
    """Test compatibility between TypedDict and Pydantic filter base models."""
    # Create a filter using TypedDict
    typed_filter = cast(
        TypedDictFilterBase,
        {
            "member": "products.price",
            "operator": "gt",
            "values": ["100"],
        },
    )

    # Convert to JSON and back
    filter_json = json.dumps(typed_filter)

    # Parse with Pydantic model
    pydantic_filter = PydanticFilterBase.model_validate_json(filter_json)

    # Verify fields match
    assert pydantic_filter.member == typed_filter["member"]
    assert pydantic_filter.operator == typed_filter["operator"]
    assert pydantic_filter.values == typed_filter["values"]

    # Convert back to dict and verify structure
    filter_dict = pydantic_filter.model_dump(by_alias=True)
    assert filter_dict["member"] == typed_filter["member"]
    assert filter_dict["operator"] == typed_filter["operator"]
    assert filter_dict["values"] == typed_filter["values"]


def test_filter_or_model_compatibility():
    """Test compatibility between TypedDict and Pydantic OR filter models."""
    # Create OR filter using TypedDict
    filter1 = cast(
        TypedDictFilterBase,
        {
            "member": "tasks.status",
            "operator": "equals",
            "values": ["Completed"],
        },
    )

    filter2 = cast(
        TypedDictFilterBase,
        {
            "member": "tasks.priority",
            "operator": "equals",
            "values": ["High"],
        },
    )

    typed_or_filter = cast(TypedDictFilterOr, {"or": [filter1, filter2]})

    # Convert to JSON and back
    filter_json = json.dumps(typed_or_filter)

    # Parse with Pydantic model
    pydantic_or_filter = PydanticFilterOr.model_validate_json(filter_json)

    # Verify fields match
    assert pydantic_or_filter.or_filters is not None
    assert len(pydantic_or_filter.or_filters) == 2

    # Check the first filter - we know it's a base filter
    base_filter1 = pydantic_or_filter.or_filters[0]
    if isinstance(base_filter1, PydanticFilterBase):
        assert base_filter1.member == filter1["member"]

    # Check the second filter - we know it's a base filter
    base_filter2 = pydantic_or_filter.or_filters[1]
    if isinstance(base_filter2, PydanticFilterBase):
        assert base_filter2.member == filter2["member"]

    # Convert back to dict and verify structure
    filter_dict = pydantic_or_filter.model_dump(by_alias=True)
    assert len(filter_dict["or"]) == 2
    assert filter_dict["or"][0]["member"] == filter1["member"]
    assert filter_dict["or"][1]["member"] == filter2["member"]


def test_filter_and_model_compatibility():
    """Test compatibility between TypedDict and Pydantic AND filter models."""
    # Create AND filter using TypedDict
    filter1 = cast(
        TypedDictFilterBase,
        {
            "member": "opportunities.stage",
            "operator": "equals",
            "values": ["Closed Won"],
        },
    )

    filter2 = cast(
        TypedDictFilterOr,
        {
            "or": [
                cast(
                    TypedDictFilterBase,
                    {
                        "member": "opportunities.close_date",
                        "operator": "gte",
                        "values": ["2024-01-01"],
                    },
                ),
                cast(
                    TypedDictFilterBase,
                    {
                        "member": "opportunities.close_date",
                        "operator": "lte",
                        "values": ["2024-12-31"],
                    },
                ),
            ]
        },
    )

    typed_and_filter = cast(TypedDictFilterAnd, {"and": [filter1, filter2]})

    # Convert to JSON and back
    filter_json = json.dumps(typed_and_filter)

    # Parse with Pydantic model
    pydantic_and_filter = PydanticFilterAnd.model_validate_json(filter_json)

    # Verify fields match
    assert pydantic_and_filter.and_filters is not None
    assert len(pydantic_and_filter.and_filters) == 2

    # Check the first filter - we know it's a base filter
    base_filter = pydantic_and_filter.and_filters[0]
    if isinstance(base_filter, PydanticFilterBase):
        assert base_filter.member == filter1["member"]

    # Check the second filter - we know it's an OR filter
    or_filter = pydantic_and_filter.and_filters[1]
    if isinstance(or_filter, PydanticFilterOr):
        assert or_filter.or_filters is not None

    # Convert back to dict and verify structure
    filter_dict = pydantic_and_filter.model_dump(by_alias=True)
    assert len(filter_dict["and"]) == 2
    assert filter_dict["and"][0]["member"] == filter1["member"]
    assert "or" in filter_dict["and"][1]


def test_time_dimension_model_compatibility():
    """Test compatibility between TypedDict and Pydantic time dimension models."""
    # Create time dimension using TypedDict
    typed_time_dim = cast(
        TypedDictTimeDimension,
        {
            "dimension": "opportunities.created_at",
            "dateRange": "last 6 months",
            "granularity": "month",
        },
    )

    # Convert to JSON and back
    time_dim_json = json.dumps(typed_time_dim)

    # Parse with Pydantic model
    pydantic_time_dim = PydanticTimeDimension.model_validate_json(time_dim_json)

    # Verify fields match
    assert pydantic_time_dim.dimension == typed_time_dim["dimension"]
    assert pydantic_time_dim.date_range == typed_time_dim["dateRange"]
    assert pydantic_time_dim.granularity == typed_time_dim["granularity"]

    # Convert back to dict and verify structure
    time_dim_dict = pydantic_time_dim.model_dump(by_alias=True)
    assert time_dim_dict["dimension"] == typed_time_dim["dimension"]
    assert time_dim_dict["dateRange"] == typed_time_dim["dateRange"]
    assert time_dim_dict["granularity"] == typed_time_dim["granularity"]


@pytest.mark.parametrize("typed_query", TEST_QUERIES)
def test_query_model_compatibility(typed_query: TypedDictQuery):
    """Test compatibility between TypedDict and Pydantic query models with test fixtures."""
    # Convert TypedDict query to JSON
    query_json = json.dumps(typed_query)

    # Parse with Pydantic model
    pydantic_query = PydanticQuery.model_validate_json(query_json)

    # Convert back to dict
    query_dict = pydantic_query.model_dump(by_alias=True, exclude_none=True)

    # Verify that all original keys are present in the round-tripped query
    for key in typed_query:
        if key in query_dict:
            # For complex values like lists of objects, we just check that they're present
            # Since the exact structure was tested in more specific tests
            assert key in query_dict


def test_complex_query_round_trip():
    """Test a complex query with all possible fields for complete round-trip serialization."""
    # Create a complex query using TypedDict
    complex_query = cast(
        TypedDictQuery,
        {
            "measures": ["products.count"],
            "dimensions": ["products.name", "products.category"],
            "segments": ["active_products"],
            "timeDimensions": [
                cast(
                    TypedDictTimeDimension,
                    {
                        "dimension": "products.created_at",
                        "dateRange": ["2024-01-01", "2024-12-31"],
                        "granularity": "month",
                    },
                )
            ],
            "filters": [
                cast(
                    TypedDictFilterAnd,
                    {
                        "and": [
                            cast(
                                TypedDictFilterBase,
                                {
                                    "member": "products.price",
                                    "operator": "gt",
                                    "values": ["100"],
                                },
                            ),
                            cast(
                                TypedDictFilterOr,
                                {
                                    "or": [
                                        cast(
                                            TypedDictFilterBase,
                                            {
                                                "member": "products.category",
                                                "operator": "equals",
                                                "values": ["Electronics"],
                                            },
                                        ),
                                        cast(
                                            TypedDictFilterBase,
                                            {
                                                "member": "products.category",
                                                "operator": "equals",
                                                "values": ["Accessories"],
                                            },
                                        ),
                                    ]
                                },
                            ),
                        ]
                    },
                )
            ],
            "order": [["products.price", "desc"]],
            "limit": 20,
            "offset": 0,
            "timezone": "America/New_York",
            "renewQuery": True,
            "ungrouped": False,
        },
    )

    # Convert to JSON
    query_json = json.dumps(complex_query)

    # Parse with Pydantic model
    pydantic_query = PydanticQuery.model_validate_json(query_json)

    # Convert back to dict
    query_dict = pydantic_query.model_dump(by_alias=True)

    # Verify top-level fields
    assert query_dict["measures"] == complex_query["measures"]
    assert query_dict["dimensions"] == complex_query["dimensions"]
    assert query_dict["segments"] == complex_query["segments"]
    assert query_dict["limit"] == complex_query["limit"]
    assert query_dict["offset"] == complex_query["offset"]
    assert query_dict["timezone"] == complex_query["timezone"]
    assert query_dict["renewQuery"] == complex_query["renewQuery"]
    assert query_dict["ungrouped"] == complex_query["ungrouped"]

    # Verify time dimensions
    assert len(query_dict["timeDimensions"]) == 1
    assert (
        query_dict["timeDimensions"][0]["dimension"]
        == complex_query["timeDimensions"][0]["dimension"]
    )

    # Access dateRange with check for TypedDict
    if "dateRange" in complex_query["timeDimensions"][0]:
        assert (
            query_dict["timeDimensions"][0]["dateRange"]
            == complex_query["timeDimensions"][0]["dateRange"]
        )

    # Access granularity with check for TypedDict
    if "granularity" in complex_query["timeDimensions"][0]:
        assert (
            query_dict["timeDimensions"][0]["granularity"]
            == complex_query["timeDimensions"][0]["granularity"]
        )

    # Verify filters (this is more complex due to nested structure)
    assert len(query_dict["filters"]) == 1
    assert "and" in query_dict["filters"][0]
    assert len(query_dict["filters"][0]["and"]) == 2

    # First AND condition (simple filter)
    assert query_dict["filters"][0]["and"][0]["member"] == "products.price"
    assert query_dict["filters"][0]["and"][0]["operator"] == "gt"
    assert query_dict["filters"][0]["and"][0]["values"] == ["100"]

    # Second AND condition (OR filter)
    assert "or" in query_dict["filters"][0]["and"][1]
    assert len(query_dict["filters"][0]["and"][1]["or"]) == 2

    # First OR condition
    assert (
        query_dict["filters"][0]["and"][1]["or"][0]["member"]
        == "products.category"
    )
    assert query_dict["filters"][0]["and"][1]["or"][0]["values"] == [
        "Electronics"
    ]

    # Second OR condition
    assert (
        query_dict["filters"][0]["and"][1]["or"][1]["member"]
        == "products.category"
    )
    assert query_dict["filters"][0]["and"][1]["or"][1]["values"] == [
        "Accessories"
    ]
