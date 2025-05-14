"""
Cube.dev HTTP Client - Custom Response Models Example

This example demonstrates how to create and use custom response models
with the cube-http-client library to handle extended Cube.js responses.
"""

import asyncio
from typing import Any

from pydantic import Field

import cube_http
from cube_http.types.v1 import V1LoadResponse, V1MetaResponse, V1SqlResponse

# ------ Custom Load Response Models ------


class CustomLoadResponse(V1LoadResponse):
    """Extended load response model with additional custom fields."""

    # Add a top-level custom field
    execution_details: dict[str, Any] = Field(
        default_factory=dict,
        alias="executionDetails",
        description="Extended execution details from a modified Cube.js server.",
    )


# ------ Custom SQL Response Model ------


class CustomSqlResponse(V1SqlResponse):
    """Extended SQL response model with additional custom fields."""

    optimizer_info: dict[str, Any] = Field(
        default_factory=dict,
        alias="optimizerInfo",
        description="SQL query optimizer information from an extended Cube.js server.",
    )


# ------ Custom Meta Response Model ------


class CustomMetaResponse(V1MetaResponse):
    """Extended metadata response model with additional custom fields."""

    schema_version: str | None = Field(
        default=None,
        alias="schemaVersion",
        description="Version information for the data schema.",
    )
    deployment_info: dict[str, Any] = Field(
        default_factory=dict,
        alias="deploymentInfo",
        description="Additional deployment information from an extended Cube.js server.",
    )


def synchronous_example():
    """Demonstrate custom response models with synchronous client."""
    print("\n===== Synchronous Custom Response Models Example =====")

    # Initialize client
    cube = cube_http.Client(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
        }
    )

    # 1. Load query with custom response model
    print("\n----- Load Query with Custom Response Model -----")
    try:
        response = cube.v1.load(
            {
                "query": {
                    "measures": ["tasks.count"],
                    "dimensions": ["tasks.status"],
                }
            },
            response_model=CustomLoadResponse,
        )

        print(f"Data rows: {len(response.results[0].data)}")

        # Access standard fields
        print("Standard fields available:")
        print(f"  - Query type: {response.query_type}")
        print(f"  - Results count: {len(response.results)}")

        # Access custom fields (will use default values if not provided by server)
        print("Custom fields (with default values if not in response):")
        print(f"  - Execution details: {response.execution_details}")

    except Exception as e:
        print(f"Error: {e}")

    # 2. SQL query with custom response model
    print("\n----- SQL Query with Custom Response Model -----")
    try:
        sql_response = cube.v1.sql(
            {
                "query": {
                    "measures": ["tasks.count"],
                    "dimensions": ["tasks.status"],
                }
            },
            response_model=CustomSqlResponse,
        )

        # Access standard fields
        sql_query, params = sql_response.sql.sql
        print(f"SQL query generated: {sql_query[:60]}...")
        print(f"Parameters: {params}")

        # Access custom fields
        print(f"Optimizer info: {sql_response.optimizer_info}")

    except Exception as e:
        print(f"Error: {e}")

    # 3. Meta query with custom response model
    print("\n----- Meta Query with Custom Response Model -----")
    try:
        meta_response = cube.v1.meta(response_model=CustomMetaResponse)
        assert meta_response.cubes

        # Access standard fields
        print(f"Available cubes: {[c.name for c in meta_response.cubes[:3]]}...")

        # Access custom fields
        print(f"Schema version: {meta_response.schema_version}")
        print(f"Deployment info: {meta_response.deployment_info}")

    except Exception as e:
        print(f"Error: {e}")


async def async_example():
    """Demonstrate custom response models with asynchronous client."""
    print("\n===== Asynchronous Custom Response Models Example =====")

    # Initialize client
    cube = cube_http.AsyncClient(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
        }
    )

    # 1. Load query with custom response model
    print("\n----- Load Query with Custom Response Model -----")
    try:
        response = await cube.v1.load(
            {
                "query": {
                    "measures": ["tasks.count"],
                    "dimensions": ["tasks.priority"],
                }
            },
            response_model=CustomLoadResponse,
        )

        print(f"Data rows: {len(response.results[0].data)}")

        # Access standard fields
        print("Standard fields available:")
        print(f"  - Query type: {response.query_type}")
        print(f"  - Results count: {len(response.results)}")

        # Access custom fields (will use default values if not provided by server)
        print("Custom fields (with default values if not in response):")
        print(f"  - Execution details: {response.execution_details}")

    except Exception as e:
        print(f"Error: {e}")

    # 2. Run multiple queries in parallel with custom response models
    print("\n----- Parallel Queries with Custom Response Models -----")
    try:
        # Define three queries with different custom response models
        load_query = cube.v1.load(
            {
                "query": {
                    "measures": ["tasks.count"],
                    "dimensions": ["tasks.status"],
                }
            },
            response_model=CustomLoadResponse,
        )

        sql_query = cube.v1.sql(
            {
                "query": {
                    "measures": ["tasks.count"],
                }
            },
            response_model=CustomSqlResponse,
        )

        meta_query = cube.v1.meta(response_model=CustomMetaResponse)

        # Run all three queries in parallel
        load_response, sql_response, meta_response = await asyncio.gather(
            load_query, sql_query, meta_query
        )

        print("Successfully ran 3 parallel queries with custom response models")
        print(f"Load data rows: {len(load_response.results[0].data)}")
        print(f"SQL query: {sql_response.sql.sql[0][:40]}...")
        print(f"Meta cubes count: {len(meta_response.cubes or [])}")

    except Exception as e:
        print(f"Error in parallel queries: {e}")


if __name__ == "__main__":
    # Run synchronous example
    synchronous_example()

    # Run asynchronous example
    asyncio.run(async_example())
