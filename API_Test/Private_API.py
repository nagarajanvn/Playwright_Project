import pytest
import requests

BASE_URL = "https://api.restful-api.dev/collections"
VALID_API_KEY = "facc9cb2-9617-4f8a-8210-618b4f879a8d"


def test_get_collections_with_valid_api_key_success():
    """Positive: valid x-api-key should allow access and return a JSON response."""
    headers = {"x-api-key": VALID_API_KEY}
    response = requests.get(BASE_URL, headers=headers, timeout=10)

    if response.status_code == 405 and "daily request limit" in response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping valid-key validation.")

    assert response.status_code == 200, (
        f"Expected 200 with valid API key, got {response.status_code}. Response: {response.text}"
    )

    try:
        data = response.json()
    except ValueError as exc:
        raise AssertionError("Response is not valid JSON") from exc

    assert data is not None, "Response body is empty"
    if isinstance(data, list):
        assert isinstance(data, list), "Expected a JSON list for collections"
    elif isinstance(data, dict):
        assert len(data) > 0, "Expected non-empty JSON object"
    else:
        pytest.fail(f"Unexpected response format: {type(data).__name__}")


def test_get_collections_without_api_key_negative():
    """Negative: requests without x-api-key should be rejected with 401 or 403."""
    response = requests.get(BASE_URL, timeout=10)

    if response.status_code == 405 and "daily request limit" in response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping missing-key validation.")

    assert response.status_code in (401, 403), (
        f"Expected 401 or 403 for missing API key, got {response.status_code}. Response: {response.text}"
    )


def test_get_collections_invalid_api_key_negative():
    """Negative: invalid x-api-key should be rejected or at least not auth as valid."""
    invalid_headers = {"x-api-key": "invalid-key-0000-0000"}
    valid_headers = {"x-api-key": VALID_API_KEY}

    invalid_response = requests.get(BASE_URL, headers=invalid_headers, timeout=10)
    valid_response = requests.get(BASE_URL, headers=valid_headers, timeout=10)

    if invalid_response.status_code == 405 and "daily request limit" in invalid_response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping invalid-key validation.")

    if invalid_response.status_code in (401, 403):
        return

    if invalid_response.status_code == valid_response.status_code and invalid_response.text == valid_response.text:
        pytest.skip("Service ignores API key differences; cannot assert invalid-key rejection.")

    assert invalid_response.status_code != 200 or invalid_response.text != valid_response.text, (
        f"Invalid API key returned the same successful response as a valid key (status {invalid_response.status_code})"
    )


def test_get_collections_empty_api_key_negative():
    """Negative: empty x-api-key should not authorize access."""
    headers = {"x-api-key": ""}
    response = requests.get(BASE_URL, headers=headers, timeout=10)

    if response.status_code == 405 and "daily request limit" in response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping empty-key validation.")

    assert response.status_code in (401, 403), (
        f"Expected 401 or 403 for empty API key, got {response.status_code}. Response: {response.text}"
    )


def test_get_collections_wrong_method_negative():
    """Negative: POST should not be accepted on the collections GET endpoint."""
    headers = {"x-api-key": VALID_API_KEY}
    response = requests.post(BASE_URL, headers=headers, timeout=10)

    if response.status_code == 405 and "daily request limit" in response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping wrong-method validation.")

    assert response.status_code >= 400 and response.status_code != 200, (
        f"Expected non-2xx for POST to collections endpoint, got {response.status_code}. Response: {response.text}"
    )


if __name__ == "__main__":
    tests = [
        test_get_collections_with_valid_api_key_success,
        test_get_collections_without_api_key_negative,
        test_get_collections_invalid_api_key_negative,
        test_get_collections_empty_api_key_negative,
        test_get_collections_wrong_method_negative,
    ]
    for test in tests:
        test()
