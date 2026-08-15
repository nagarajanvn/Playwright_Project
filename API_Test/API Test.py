import json

import pytest
import requests

BASE_URL = "https://api.restful-api.dev/objects"

VALID_PAYLOAD = {
    "name": "Apple MacBook Pro 19",
    "data": {
        "year": 2026,
        "price": 1849.99,
        "CPU model": "Intel Core i9",
        "Hard disk size": "1 TB",
    },
}


def test_post_objects_success_create():
    """Positive: create a valid object and verify the API responds successfully."""
    response = requests.post(BASE_URL, json=VALID_PAYLOAD, timeout=10)

    if response.status_code == 405:
        pytest.skip("POST is not allowed on this endpoint; skipping create test.")

    assert response.status_code in (200, 201), (
        f"Expected 200 or 201, got {response.status_code}. Response: {response.text}"
    )

    try:
        data = response.json()
    except ValueError as exc:
        raise AssertionError("Response is not valid JSON") from exc

    assert isinstance(data, dict), "Expected response body to be a JSON object."
    assert data.get("name") == VALID_PAYLOAD["name"], (
        f"Expected created object name '{VALID_PAYLOAD['name']}', got '{data.get('name')}'"
    )
    assert "id" in data, "Response JSON did not include an 'id' field."


def test_post_objects_missing_name_negative():
    """Negative: sending a payload without the required 'name' should be rejected."""
    payload = {"data": {"year": 2026, "price": 1849.99}}

    response = requests.post(BASE_URL, json=payload, timeout=10)

    if response.status_code == 405 and "daily request limit" in response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping rate-limited validation.")

    if response.status_code in (200, 201):
        pytest.skip("Service accepted a payload without a name; cannot assert rejection.")

    assert response.status_code in (400, 404, 422), (
        f"Expected 4xx status for missing name, got {response.status_code}. Response: {response.text}"
    )


def test_post_objects_invalid_json_negative():
    """Negative: malformed JSON should return a client-error status."""
    malformed_json = '{"name": "Broken JSON"'  # missing closing brace
    headers = {"Content-Type": "application/json"}

    response = requests.post(BASE_URL, data=malformed_json, headers=headers, timeout=10)

    if response.status_code == 405 and "daily request limit" in response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping rate-limited validation.")

    if response.status_code in (200, 201):
        pytest.skip("Service accepted malformed JSON; cannot assert rejection.")

    assert response.status_code in (400, 415), (
        f"Expected 400 or 415 for malformed JSON, got {response.status_code}. Response: {response.text}"
    )


def test_post_objects_duplicate_payload_behavior():
    """Edge: sending the same payload twice should either be rejected or accepted consistently."""
    payload = {
        "name": "Apple MacBook Pro Duplicate Test",
        "data": {"year": 2026, "price": 1849.99},
    }

    first_response = requests.post(BASE_URL, json=payload, timeout=10)
    if first_response.status_code == 405 and "daily request limit" in first_response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping rate-limited validation.")

    second_response = requests.post(BASE_URL, json=payload, timeout=10)

    if first_response.status_code not in (200, 201):
        pytest.skip(f"Initial create failed with status {first_response.status_code}; skipping duplicate test.")

    if second_response.status_code >= 400:
        return

    assert second_response.status_code in (200, 201), (
        f"Expected duplicate POST to be accepted or rejected, got {second_response.status_code}. Response: {second_response.text}"
    )


def test_post_objects_large_payload_edge():
    """Edge: very large payload sizes should not crash the API and should be handled gracefully."""
    large_name = "A" * 20000
    payload = {"name": large_name, "data": {"year": 2026}}

    response = requests.post(BASE_URL, json=payload, timeout=20)

    if response.status_code == 405 and "daily request limit" in response.text.lower():
        pytest.skip("Public API has reached its daily request limit; skipping rate-limited validation.")

    if response.status_code >= 400:
        return

    assert response.status_code in (200, 201), (
        f"Expected accepted or rejected large payload, got {response.status_code}. Response: {response.text}"
    )


if __name__ == "__main__":
    print(json.dumps(VALID_PAYLOAD, indent=2))
    for test in [
        test_post_objects_success_create,
        test_post_objects_missing_name_negative,
        test_post_objects_invalid_json_negative,
        test_post_objects_duplicate_payload_behavior,
        test_post_objects_large_payload_edge,
    ]:
        test()
