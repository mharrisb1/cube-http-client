import json

import httpx

from cube_http.exc.v1._base import V1BaseError


def test_v1_base_error_from_response_valid_json():
    """Test from_response with valid JSON error response."""
    # Create a mock response with valid JSON
    response_data = {"error": "Something went wrong"}
    response = httpx.Response(
        status_code=400,
        content=json.dumps(response_data).encode(),
        headers={"content-type": "application/json"},
    )

    error = V1BaseError.from_response(response)

    assert error.status_code == 400
    assert error.error == "Something went wrong"
    assert str(error) == "Returned status code 400. Reason: Something went wrong"


def test_v1_base_error_from_response_invalid_json():
    """Test from_response with invalid JSON response."""
    # Create a mock response with invalid JSON
    response = httpx.Response(
        status_code=500,
        content=b"Internal Server Error",
        headers={"content-type": "text/plain"},
    )

    error = V1BaseError.from_response(response)

    assert error.status_code == 500
    assert error.error == "Internal Server Error"
    assert (
        str(error) == "Returned status code 500. Reason: Internal Server Error"
    )


def test_v1_base_error_from_response_validation_error():
    """Test from_response with JSON that fails validation."""
    # Create a mock response with JSON that doesn't match V1Error model
    response_data = {"message": "Wrong field name"}
    response = httpx.Response(
        status_code=422,
        content=json.dumps(response_data).encode(),
        headers={"content-type": "application/json"},
    )

    error = V1BaseError.from_response(response)

    assert error.status_code == 422
    assert error.error == "Invalid response from server"
    assert (
        str(error)
        == "Returned status code 422. Reason: Invalid response from server"
    )


def test_v1_base_error_from_response_empty_response():
    """Test from_response with empty response."""
    response = httpx.Response(status_code=204, content=b"", headers={})

    error = V1BaseError.from_response(response)

    assert error.status_code == 204
    assert error.error == ""
    assert str(error) == "Returned status code 204. Reason: "


def test_v1_base_error_from_response_malformed_json():
    """Test from_response with malformed JSON."""
    response = httpx.Response(
        status_code=400,
        content=b'{"error": "missing quote}',
        headers={"content-type": "application/json"},
    )

    error = V1BaseError.from_response(response)

    assert error.status_code == 400
    assert error.error == '{"error": "missing quote}'
    assert (
        str(error)
        == 'Returned status code 400. Reason: {"error": "missing quote}'
    )
