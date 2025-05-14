"""
Cube.dev HTTP Client - Async Quickstart Example

This example demonstrates the asynchronous usage of the cube-http-client library
for interacting with a Cube.dev REST API.
"""

import asyncio

import cube_http
from cube_http.exc import V1LoadError, V1MetaError, V1SqlError


async def get_metadata(cube: cube_http.AsyncClient):
    """Retrieve and display metadata about available cubes asynchronously."""
    try:
        meta_resp = await cube.v1.meta()

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


async def query_data(cube: cube_http.AsyncClient):
    """Execute a data query with filters and dimensions asynchronously."""
    try:
        print("\n=== Query Results ===")
        load_resp = await cube.v1.load(
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


async def get_sql(cube: cube_http.AsyncClient):
    """Get the SQL that would be generated for a query asynchronously."""
    try:
        print("\n=== SQL Query ===")
        sql_resp = await cube.v1.sql(
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


async def error_handling_example(cube: cube_http.AsyncClient):
    """Demonstrates error handling for various scenarios asynchronously."""
    print("\n=== Error Handling Examples ===")

    # Example 1: Invalid measure
    try:
        await cube.v1.load({"query": {"measures": ["invalid.measure"]}})
    except V1LoadError as e:
        print(f"Invalid measure error: {e}")

    # Example 2: Malformed query
    try:
        await cube.v1.load({"query": {"invalid_key": "invalid_value"}})  # type: ignore
    except V1LoadError as e:
        print(f"Malformed query error: {e}")


async def parallel_requests_example(cube: cube_http.AsyncClient):
    """Demonstrates running multiple queries in parallel using asyncio."""
    print("\n=== Parallel Requests Example ===")

    # Define several queries to run in parallel
    query1 = cube.v1.load(
        {
            "query": {
                "measures": ["tasks.count"],
                "dimensions": ["tasks.status"],
            }
        }
    )

    query2 = cube.v1.load(
        {
            "query": {
                "measures": ["tasks.count"],
                "dimensions": ["tasks.priority"],
            }
        }
    )

    # Run all queries concurrently
    start_time = asyncio.get_event_loop().time()
    results = await asyncio.gather(query1, query2, return_exceptions=True)
    end_time = asyncio.get_event_loop().time()

    print(
        f"Completed 2 parallel requests in {end_time - start_time:.2f} seconds"
    )

    # Process results
    for i, result in enumerate(results):
        if isinstance(result, BaseException):
            print(f"Request {i + 1} failed: {result}")
        else:
            print(f"Request {i + 1} successful")

    # Access data from the first query (tasks by status)
    if not isinstance(results[0], BaseException):
        print("\nTasks by Status:")
        for record in results[0].results[0].data:
            status = record.get("tasks.status", "N/A")
            count = record.get("tasks.count", 0)
            print(f"  {status}: {count}")

    # Access data from the second query (tasks by priority)
    if not isinstance(results[1], BaseException):
        print("\nTasks by Priority:")
        for record in results[1].results[0].data:
            priority = record.get("tasks.priority", "N/A")
            count = record.get("tasks.count", 0)
            print(f"  {priority}: {count}")


async def main():
    """Main async function to run all examples."""
    # Initialize the async client with configuration options
    cube = cube_http.AsyncClient(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
            "timeout": 30.0,
            "max_retries": 2,
        }
    )

    # Run example functions
    await get_metadata(cube)
    await query_data(cube)
    await get_sql(cube)
    await error_handling_example(cube)
    await parallel_requests_example(cube)


if __name__ == "__main__":
    asyncio.run(main())
