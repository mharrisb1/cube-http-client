"""
Cube.dev HTTP Client - Quickstart Example

This example demonstrates the basic usage of the cube-http-client library
for interacting with a Cube.dev REST API.
"""

import cube_http
from cube_http.exc import V1LoadError, V1MetaError, V1SqlError


def get_metadata(cube: cube_http.Client):
    """Retrieve and display metadata about available cubes."""
    try:
        meta_resp = cube.v1.meta()

        if not meta_resp.cubes:
            print("No cubes found")
            return

        # Print available cubes
        print("\n=== Metadata ===")
        print(f"Available cubes: {[cube.name for cube in meta_resp.cubes]}")

        # Print details about a specific cube (tasks)
        for cube_info in meta_resp.cubes:
            if cube_info.name == "tasks":
                print("\nDetails for 'tasks' cube:")
                print(f"  Measures: {[m.name for m in cube_info.measures]}")
                print(f"  Dimensions: {[d.name for d in cube_info.dimensions]}")

                # Display measure types
                print("\n  Measure details:")
                for measure in cube_info.measures:
                    print(
                        f"    {measure.name} ({measure.type}): {measure.description or 'No description'}"
                    )

                # Display dimension types
                print("\n  Dimension details:")
                for dimension in cube_info.dimensions:
                    print(
                        f"    {dimension.name} ({dimension.type}): {dimension.description or 'No description'}"
                    )

    except V1MetaError as e:
        print(f"Error fetching metadata: {e}")


def query_data(cube: cube_http.Client):
    """Execute a data query with filters and dimensions."""
    try:
        print("\n=== Query Results ===")
        load_resp = cube.v1.load(
            {
                "query": {
                    "measures": ["tasks.count"],
                    "dimensions": ["tasks.status", "tasks.priority"],
                    "filters": [
                        {
                            "or": [
                                {
                                    "member": "tasks.status",
                                    "operator": "equals",
                                    "values": ["Completed"],
                                },
                                {
                                    "member": "tasks.priority",
                                    "operator": "equals",
                                    "values": ["High"],
                                },
                            ]
                        }
                    ],
                    "limit": 10,
                }
            }
        )

        # Access result data
        results = load_resp.results[0]
        records = results.data

        # Print total count and records
        print(f"Found {len(records)} records")

        # Print data in a readable format
        print("\nResults:")
        for i, record in enumerate(records, 1):
            status = record.get("tasks.status", "N/A")
            priority = record.get("tasks.priority", "N/A")
            count = record.get("tasks.count", 0)
            print(
                f"  {i}. Status: {status}, Priority: {priority}, Count: {count}"
            )

        # Access annotations if available
        print("\nAnnotations:")
        annotations = results.annotation
        print(f"  Measures: {list(annotations.measures.keys())}")
        print(f"  Dimensions: {list(annotations.dimensions.keys())}")

        # Check for pre-aggregations usage
        if results.used_pre_aggregations:
            print("\nPre-aggregations used:")
            for pre_agg, details in results.used_pre_aggregations.items():
                print(f"  {pre_agg}: {details}")

    except V1LoadError as e:
        print(f"Error loading data: {e}")


def get_sql(cube: cube_http.Client):
    """Get the SQL that would be generated for a query."""
    try:
        print("\n=== SQL Query ===")
        sql_resp = cube.v1.sql(
            {
                "query": {
                    "measures": ["tasks.count"],
                    "dimensions": ["tasks.status"],
                    "timeDimensions": [
                        {"dimension": "tasks.createdAt", "granularity": "month"}
                    ],
                }
            }
        )

        # Extract SQL and parameters
        sql_query, params = sql_resp.sql.sql

        # Print the SQL query with parameters
        print("SQL Query:")
        print(f"  {sql_query}")
        print("\nParameters:")
        for i, param in enumerate(params, 1):
            print(f"  {i}. {param}")

        # Show other metadata if available
        if sql_resp.sql.data_source:
            print(f"\nData Source: {sql_resp.sql.data_source}")

        if sql_resp.sql.pre_aggregations:
            print("\nPre-aggregations:")
            for pre_agg in sql_resp.sql.pre_aggregations:
                print(f"  {pre_agg}")

    except V1SqlError as e:
        print(f"Error fetching SQL: {e}")


def error_handling_example(cube: cube_http.Client):
    """Demonstrates error handling for various scenarios."""
    print("\n=== Error Handling Examples ===")

    # Example 1: Invalid measure
    try:
        cube.v1.load({"query": {"measures": ["invalid.measure"]}})
    except V1LoadError as e:
        print(f"Invalid measure error: {e}")

    # Example 2: Malformed query
    try:
        cube.v1.load({"query": {"invalid_key": "invalid_value"}})  # type: ignore
    except V1LoadError as e:
        print(f"Malformed query error: {e}")


if __name__ == "__main__":
    # Initialize the client with configuration options
    cube = cube_http.Client(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
            "timeout": 30.0,
            "max_retries": 2,
        }
    )

    # Run example functions
    get_metadata(cube)
    query_data(cube)
    get_sql(cube)
    error_handling_example(cube)
