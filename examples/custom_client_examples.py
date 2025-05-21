"""
Cube.dev HTTP Client - Custom Client Examples

This example demonstrates how to use custom HTTPX clients with the cube-http-client library.
"""

import httpx

import cube_http
from cube_http.exc import V1LoadError


def basic_custom_client_example():
    """Demonstrate using a fully configured custom HTTPX client."""
    print("\n=== Basic Custom Client Example ===")

    # Create a fully configured custom HTTPX client
    custom_client = httpx.Client(
        base_url="http://localhost:4000/cubejs-api",
        headers={
            "Authorization": "i9f5e76b519a44b060daa33e78c5de170",
            "Content-Type": "application/json",
            "User-Agent": "CustomClient/1.0",
        },
        timeout=30.0,
    )

    # Initialize the Cube client with just the custom client
    # No need to duplicate options that are already set on the custom client
    cube = cube_http.Client({"http_client": custom_client})

    try:
        # Use the client as normal
        response = cube.v1.meta()
        print(f"Retrieved metadata for {len(response.cubes or [])} cubes")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the client when done
        cube.close()


def partial_custom_client_example():
    """Demonstrate using a partially configured custom HTTPX client with merged options."""
    print("\n=== Partial Custom Client Example ===")

    # Create a custom HTTPX client with some settings
    custom_client = httpx.Client(
        # Custom settings only
        headers={
            "User-Agent": "CustomClient/1.0",
            "X-Custom-Header": "custom-value",
        },
        timeout=15.0,
    )

    # Initialize with the custom client and provide missing required options
    cube = cube_http.Client(
        {
            "http_client": custom_client,
            # Required options that aren't in the custom client
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
            # Additional options
            "default_headers": {
                "X-Analytics-ID": "custom-example",
            },
        }
    )

    try:
        # Execute a query
        print("Executing query with merged client options...")
        load_resp = cube.v1.load(
            {
                "query": {
                    "measures": ["tasks.count"],
                    "dimensions": ["tasks.status"],
                }
            }
        )
        print(f"Query returned {len(load_resp.results[0].data)} records")

        # Verify the headers were merged properly
        print("\nClient headers:")
        for key, value in custom_client.headers.items():
            print(f"  {key}: {value}")

    except V1LoadError as e:
        print(f"Query error: {e}")
    finally:
        cube.close()


def custom_client_with_middleware():
    """Demonstrate using a custom HTTPX client with middleware."""
    print("\n=== Custom Client with Middleware Example ===")

    # Create a custom transport with logging middleware
    class LoggingTransport(httpx.HTTPTransport):
        def handle_request(self, request: httpx.Request):
            print(f">> Request: {request.method} {request.url}")
            response = super().handle_request(request)
            print(f"<< Response: {response.status_code}")
            return response

    # Create a custom client with the logging transport
    custom_client = httpx.Client(
        transport=LoggingTransport(retries=3),
    )

    # Initialize with the custom client and required options
    cube = cube_http.Client(
        {
            "http_client": custom_client,
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
        }
    )

    try:
        # The request and response will be logged by our custom transport
        print("Executing query with custom transport...")
        cube.v1.meta()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cube.close()


if __name__ == "__main__":
    # Run all examples
    basic_custom_client_example()
    partial_custom_client_example()
    custom_client_with_middleware()
