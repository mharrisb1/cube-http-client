import httpx
import pytest

import cube_http


def test_optional_fields_with_custom_client():
    """Test that fields are optional when providing a custom client."""
    # Create a custom client with all necessary configuration
    custom_client = httpx.Client(
        base_url="http://localhost:4000/cubejs-api",
        headers={
            "Authorization": "test-token",
            "Content-Type": "application/json",
            "X-Custom-Header": "custom-value",
        },
    )

    # Initialize with only the custom client
    cube = cube_http.Client({"http_client": custom_client})

    # Verify the client was properly initialized
    assert cube.http_client == custom_client
    assert cube.http_client.base_url == httpx.URL(
        "http://localhost:4000/cubejs-api/"
    )
    assert cube.http_client.headers["authorization"] == "test-token"
    assert cube.http_client.headers["x-custom-header"] == "custom-value"


def test_merge_options_with_custom_client():
    """Test that options are merged with the custom client."""
    # Create a custom client with partial configuration
    custom_client = httpx.Client(
        headers={
            "Content-Type": "application/json",
            "X-Custom-Header": "custom-value",
        },
    )

    # Initialize with custom client and additional options
    cube = cube_http.Client(
        {
            "http_client": custom_client,
            "url": "http://localhost:4000/cubejs-api",
            "token": "new-token",
            "default_headers": {"X-New-Header": "new-value"},
        }
    )

    # Verify the client was properly updated with the new options
    assert cube.http_client == custom_client
    assert cube.http_client.base_url == httpx.URL(
        "http://localhost:4000/cubejs-api/"
    )
    assert cube.http_client.headers["authorization"] == "new-token"
    assert cube.http_client.headers["content-type"] == "application/json"
    assert cube.http_client.headers["x-custom-header"] == "custom-value"
    assert cube.http_client.headers["x-new-header"] == "new-value"


def test_authorization_header_extraction():
    """Test that token is extracted from Authorization header."""
    # Create a custom client with token in Authorization header
    custom_client = httpx.Client(
        base_url="http://localhost:4000/cubejs-api",
        headers={
            "Authorization": "Bearer my-bearer-token",
            "Content-Type": "application/json",
        },
    )

    # Initialize with only the custom client
    cube = cube_http.Client({"http_client": custom_client})

    # Verify the token was extracted correctly
    assert cube.http_client.headers["authorization"] == "Bearer my-bearer-token"


@pytest.mark.asyncio
async def test_async_custom_client():
    """Test custom client with AsyncClient."""
    # Create a custom async client
    custom_client = httpx.AsyncClient(
        base_url="http://localhost:4000/cubejs-api",
        headers={
            "Authorization": "test-token",
            "Content-Type": "application/json",
        },
    )

    # Initialize with only the custom client
    cube = cube_http.AsyncClient({"http_client": custom_client})

    # Verify the client was properly initialized
    assert id(cube.http_client) == id(custom_client)
    assert cube.http_client.base_url == httpx.URL(
        "http://localhost:4000/cubejs-api/"
    )
    assert cube.http_client.headers["authorization"] == "test-token"

    # Clean up
    await cube.close()


def test_missing_required_fields():
    """Test that errors are raised when required fields are missing."""
    # Missing URL in both client and options
    custom_client = httpx.Client(headers={"Authorization": "test-token"})

    with pytest.raises(ValueError, match="Base URL must be provided"):
        cube_http.Client({"http_client": custom_client})

    # Missing token in both client and options
    custom_client = httpx.Client(base_url="http://localhost:4000/cubejs-api")

    with pytest.raises(ValueError, match="API token must be provided"):
        cube_http.Client({"http_client": custom_client})

    # Missing URL without custom client
    with pytest.raises(ValueError, match="Base URL must be provided"):
        cube_http.Client({"token": "test-token"})

    # Missing token without custom client
    with pytest.raises(ValueError, match="API token must be provided"):
        cube_http.Client({"url": "http://localhost:4000/cubejs-api"})


def test_client_without_changes():
    """Test that regular client usage still works."""
    cube = cube_http.Client(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "test-token",
        }
    )

    assert isinstance(cube.http_client, httpx.Client)
    assert cube.http_client.base_url == httpx.URL(
        "http://localhost:4000/cubejs-api/"
    )
    assert cube.http_client.headers["authorization"] == "test-token"
    assert cube.http_client.headers["content-type"] == "application/json"
