import asyncio
from typing import Any

import pytest
from pydantic import Field

import cube_http
from cube_http.types.v1 import (
    V1LoadRequestQuery,
    V1LoadResponse,
    V1MetaResponse,
    V1SqlResponse,
)

from .fixtures import TEST_QUERIES

# ------ Custom Response Models for Testing ------


class CustomLoadResponse(V1LoadResponse):
    """Test custom load response model."""

    custom_field: dict[str, Any] = Field(
        default_factory=dict, description="Test custom field"
    )


class CustomSqlResponse(V1SqlResponse):
    """Test custom SQL response model."""

    extra_data: dict[str, Any] = Field(
        default_factory=dict, description="Test extra data field"
    )


class CustomMetaResponse(V1MetaResponse):
    """Test custom metadata response model."""

    version_info: str | None = Field(
        default="1.0.0", description="Test version info field"
    )


# ------ Tests for Custom Response Models ------


@pytest.mark.parametrize("query", TEST_QUERIES)
def test_load_custom_model(url: str, token: str, query: V1LoadRequestQuery):
    """Test that custom response models work with load endpoint."""
    cube = cube_http.Client({"url": url, "token": token})

    # Use custom response model
    result = cube.v1.load({"query": query}, response_model=CustomLoadResponse)

    # Check that response is of the custom type
    assert isinstance(result, CustomLoadResponse)

    # Check that custom fields are accessible
    assert hasattr(result, "custom_field")
    assert isinstance(result.custom_field, dict)


@pytest.mark.parametrize(
    "query", TEST_QUERIES[:1]
)  # Just use one query for SQL tests
def test_sql_custom_model(url: str, token: str, query: V1LoadRequestQuery):
    """Test that custom response models work with SQL endpoint."""
    cube = cube_http.Client({"url": url, "token": token})

    # Use custom response model
    result = cube.v1.sql({"query": query}, response_model=CustomSqlResponse)

    # Check that response is of the custom type
    assert isinstance(result, CustomSqlResponse)

    # Check that custom fields are accessible
    assert hasattr(result, "extra_data")
    assert isinstance(result.extra_data, dict)

    # Check that standard functionality still works
    assert hasattr(result, "sql")
    assert result.sql.sql is not None

    # Verify SQL query is present
    sql_query, params = result.sql.sql
    assert isinstance(sql_query, str)
    assert isinstance(params, list)


def test_meta_custom_model(url: str, token: str):
    """Test that custom response models work with meta endpoint."""
    cube = cube_http.Client({"url": url, "token": token})

    # Use custom response model
    result = cube.v1.meta(response_model=CustomMetaResponse)

    # Check that response is of the custom type
    assert isinstance(result, CustomMetaResponse)

    # Check that custom fields are accessible
    assert hasattr(result, "version_info")
    assert result.version_info == "1.0.0"

    # Check that standard functionality still works
    assert hasattr(result, "cubes")
    assert len(result.cubes or []) > 0


# ------ Async Tests for Custom Response Models ------


@pytest.mark.asyncio
@pytest.mark.parametrize("query", TEST_QUERIES)
async def test_async_load_custom_model(
    url: str, token: str, query: V1LoadRequestQuery
):
    """Test that custom response models work with async load endpoint."""
    cube = cube_http.AsyncClient({"url": url, "token": token})

    # Use custom response model
    result = await cube.v1.load(
        {"query": query}, response_model=CustomLoadResponse
    )

    # Check that response is of the custom type
    assert isinstance(result, CustomLoadResponse)

    # Check that custom fields are accessible
    assert hasattr(result, "custom_field")
    assert isinstance(result.custom_field, dict)

    # Check that standard functionality still works
    assert len(result.results) > 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query", TEST_QUERIES[:1]
)  # Just use one query for SQL tests
async def test_async_sql_custom_model(
    url: str, token: str, query: V1LoadRequestQuery
):
    """Test that custom response models work with async SQL endpoint."""
    cube = cube_http.AsyncClient({"url": url, "token": token})

    # Use custom response model
    result = await cube.v1.sql(
        {"query": query}, response_model=CustomSqlResponse
    )

    # Check that response is of the custom type
    assert isinstance(result, CustomSqlResponse)

    # Check that standard functionality still works
    sql_query, _ = result.sql.sql
    assert isinstance(sql_query, str)


@pytest.mark.asyncio
async def test_async_meta_custom_model(url: str, token: str):
    """Test that custom response models work with async meta endpoint."""
    cube = cube_http.AsyncClient({"url": url, "token": token})

    # Use custom response model
    result = await cube.v1.meta(response_model=CustomMetaResponse)

    # Check that response is of the custom type
    assert isinstance(result, CustomMetaResponse)

    # Check that standard functionality still works
    assert len(result.cubes or []) > 0


@pytest.mark.asyncio
async def test_parallel_custom_models(url: str, token: str):
    """Test that custom response models work with parallel async requests."""
    cube = cube_http.AsyncClient({"url": url, "token": token})

    # Create three async tasks with different custom models
    load_task = cube.v1.load(
        {"query": TEST_QUERIES[0]}, response_model=CustomLoadResponse
    )

    sql_task = cube.v1.sql(
        {"query": TEST_QUERIES[0]}, response_model=CustomSqlResponse
    )

    meta_task = cube.v1.meta(response_model=CustomMetaResponse)

    # Run all three tasks in parallel
    load_result, sql_result, meta_result = await asyncio.gather(
        load_task, sql_task, meta_task
    )

    # Verify each result is of the correct custom type
    assert isinstance(load_result, CustomLoadResponse)
    assert isinstance(sql_result, CustomSqlResponse)
    assert isinstance(meta_result, CustomMetaResponse)
