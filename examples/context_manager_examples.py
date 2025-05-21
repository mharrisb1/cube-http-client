"""
Cube.dev HTTP Client - Context Manager Examples

This example demonstrates how to use the cube-http-client with context managers
for both synchronous and asynchronous clients to ensure proper resource cleanup.
"""

import asyncio

import cube_http
from cube_http.exc import V1MetaError


def sync_context_manager_example():
    """Demonstrates using the synchronous client as a context manager."""
    print("\n=== Synchronous Context Manager Example ===")

    # Initialize the client with configuration options and use as a context manager
    with cube_http.Client(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
            "timeout": 30.0,
            "max_retries": 2,
        }
    ) as client:
        # Execute queries within the context block
        print("Executing query within context manager...")
        try:
            meta_resp = client.v1.meta()
            print(f"Found {len(meta_resp.cubes or [])} cubes")

            # You can execute multiple operations within the context manager
            query_resp = client.v1.load(
                {
                    "query": {
                        "measures": ["tasks.count"],
                        "dimensions": ["tasks.status"],
                    }
                }
            )
            print(
                f"Query executed successfully, received {len(query_resp.results[0].data)} records"
            )

        except V1MetaError as e:
            print(f"Metadata error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    # The client is automatically closed when exiting the context block
    print("Context exited, client was automatically closed")

    # Attempting to use the client after the context manager has exited
    # would potentially use a closed connection
    print(
        "Note: Attempting to use the client here would be using a closed connection"
    )


async def async_context_manager_example():
    """Demonstrates using the asynchronous client as a context manager."""
    print("\n=== Asynchronous Context Manager Example ===")

    # Initialize the async client and use as an async context manager
    async with cube_http.AsyncClient(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
            "timeout": 30.0,
            "max_retries": 2,
        }
    ) as client:
        # Execute async queries within the async context block
        print("Executing async query within context manager...")
        try:
            meta_resp = await client.v1.meta()
            print(f"Found {len(meta_resp.cubes or [])} cubes")

            # Run parallel queries within the context manager
            query1 = client.v1.load(
                {
                    "query": {
                        "measures": ["tasks.count"],
                        "dimensions": ["tasks.status"],
                    }
                }
            )

            query2 = client.v1.load(
                {
                    "query": {
                        "measures": ["tasks.count"],
                        "dimensions": ["tasks.priority"],
                    }
                }
            )

            # Execute both queries in parallel
            results = await asyncio.gather(
                query1, query2, return_exceptions=True
            )
            print(f"Executed {len(results)} parallel queries")

            for i, result in enumerate(results):
                if isinstance(result, BaseException):
                    print(f"  Query {i + 1} failed: {result}")
                else:
                    print(
                        f"  Query {i + 1} returned {len(result.results[0].data)} records"
                    )

        except V1MetaError as e:
            print(f"Metadata error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    # The async client is automatically closed when exiting the context block
    print("Async context exited, client was automatically closed")


def manual_cleanup_example():
    """Demonstrates manually closing the client when not using a context manager."""
    print("\n=== Manual Cleanup Example ===")

    # Initialize the client without a context manager
    client = cube_http.Client(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
        }
    )

    try:
        # Use the client
        print("Executing query with manually managed client...")
        meta_resp = client.v1.meta()
        print(f"Found {len(meta_resp.cubes or [])} cubes")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Manually close the client when done
        print("Manually closing the client...")
        client.close()
        print("Client closed")


async def async_manual_cleanup_example():
    """Demonstrates manually closing the async client when not using a context manager."""
    print("\n=== Async Manual Cleanup Example ===")

    # Initialize the async client without a context manager
    client = cube_http.AsyncClient(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
        }
    )

    try:
        # Use the async client
        print("Executing async query with manually managed client...")
        meta_resp = await client.v1.meta()
        print(f"Found {len(meta_resp.cubes or [])} cubes")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Manually close the async client when done
        print("Manually closing the async client...")
        await client.close()
        print("Async client closed")


async def run_async_examples():
    """Run all async examples."""
    await async_context_manager_example()
    await async_manual_cleanup_example()


if __name__ == "__main__":
    # Run synchronous examples
    sync_context_manager_example()
    manual_cleanup_example()

    # Run asynchronous examples
    asyncio.run(run_async_examples())
