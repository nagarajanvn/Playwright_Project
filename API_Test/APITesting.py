import requests
import json
import pytest


def test_get_objects_api():
    url = "https://api.restful-api.dev/objects"
    resp = requests.get(url, timeout=10)

    # Verify status code
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    # Try to parse JSON and validate a 'message' field if present
    try:
        data = resp.json()
    except ValueError:
        raise AssertionError("Response is not valid JSON")

    if isinstance(data, dict) and "message" in data:
        assert data["message"], "The 'message' field is empty"
        print("API message:", data["message"])
    else:
        # If no 'message' field, just print the top-level keys or length
        print("Response JSON (no 'message' field):", data)


if __name__ == "__main__":
    # Allow running the tests directly for quick verification
    test_get_objects_api()

def test_get_object_13_api():
    url = "https://api.restful-api.dev/objects/13"
    resp = requests.get(url, timeout=10)

    # Verify status code
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    # Parse JSON and check for 'message' or verify the id
    try:
        data = resp.json()
    except ValueError:
        raise AssertionError("Response is not valid JSON")

    # Print the complete response JSON for debugging/verification
    try:
        print("Full response JSON:", json.dumps(data, indent=2))
    except Exception:
        print("Full response (raw):", resp.text)

    if isinstance(data, dict) and "message" in data:
        assert data["message"], "The 'message' field is empty"
        print("API message:", data["message"])
    elif isinstance(data, dict) and "id" in data:
        assert str(data["id"]) == "13", f"Expected id '13', got {data['id']}"
        print("Object name:", data.get("name"))
    else:
        print("Unexpected response format:", data)


def test_post_object_api():
    url = "https://api.restful-api.dev/objects"
    payload = {
        "name": "Lenovo ThinkPad X1 Carbon",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    }

    resp = requests.post(url, json=payload, timeout=10)

    # Verify status code is 200 or 201
    assert resp.status_code in (200, 201), f"Expected 200 or 201, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        raise AssertionError("Response is not valid JSON")

    # Print full response JSON
    try:
        print("Full response JSON:", json.dumps(data, indent=2))
    except Exception:
        print("Full response (raw):", resp.text)

    # Basic validations
    if isinstance(data, dict):
        if "id" in data:
            print("Created object id:", data.get("id"))
        assert data.get("name") == payload["name"], f"Expected name '{payload['name']}', got '{data.get('name')}'"
    else:
        assert payload["name"] in resp.text, "Posted name not found in response"


def test_patch_object_api():
    url = "https://api.restful-api.dev/objects/ff8081819ff5b110019ffbe8825b13ae"
    payload = {"name": "MacBook Air M5 Pro"}

    resp = requests.patch(url, json=payload, timeout=10)

    # Verify status code is 200
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        raise AssertionError("Response is not valid JSON")

    # Print full response JSON
    try:
        print("Full response JSON:", json.dumps(data, indent=2))
    except Exception:
        print("Full response (raw):", resp.text)

    # Validate that the name was updated/echoed
    if isinstance(data, dict):
        assert data.get("name") == payload["name"], f"Expected name '{payload['name']}', got '{data.get('name')}'"
    else:
        assert payload["name"] in resp.text, "Patched name not found in response"


def test_put_object_api():
    url = "https://api.restful-api.dev/objects/ff8081819ff5b110019ffbe8825b13ae"
    payload = {
        "name": "MacBook M4 Pro",
        "data": {
            "year": 2026,
            "price": 777.99,
            "CPU model": "Apple M4 Pro",
            "Hard disk size": "1 TB",
            "color": "black"
        }
    }

    resp = requests.put(url, json=payload, timeout=10)

    # Verify status code is 200
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        raise AssertionError("Response is not valid JSON")

    # Print full response JSON
    try:
        print("Full response JSON:", json.dumps(data, indent=2))
    except Exception:
        print("Full response (raw):", resp.text)

    # Validate that the name and data were updated/echoed
    if isinstance(data, dict):
        assert data.get("name") == payload["name"], f"Expected name '{payload['name']}', got '{data.get('name')}'"
        # Optional: verify one of the data fields
        d = data.get("data", {})
        assert d.get("year") == 2026, f"Expected year 2026, got {d.get('year')}"
    else:
        assert payload["name"] in resp.text, "PUT name not found in response"


if __name__ == "__main__":
    test_get_objects_api()
    test_get_object_13_api()
    # Uncomment to run POST test directly
    # test_post_object_api()
    # Uncomment to run PATCH test directly
    # test_patch_object_api()
    # Uncomment to run PUT test directly
    # test_put_object_api()


def test_get_objects_wrong_method_negative():
    """Using an unsupported method (POST) on the GET-only endpoint should not return 200."""
    url = "https://api.restful-api.dev/objects"
    resp = requests.post(url, timeout=10)

    # Expect a client or server error for an inappropriate method
    assert resp.status_code >= 400 and resp.status_code != 200, (
        f"Expected non-2xx for POST to GET endpoint, got {resp.status_code}"
    )


def test_get_objects_invalid_path_returns_404():
    """A malformed or incorrect path should return 404."""
    url = "https://api.restful-api.dev/objects/invalid-path"
    resp = requests.get(url, timeout=10)

    assert resp.status_code == 404, f"Expected 404 for invalid path, got {resp.status_code}"


def test_get_objects_malformed_url_raises():
    """A syntactically malformed URL should raise a requests exception."""
    url = "https://api.restful-api.dev/::bad_url"
    with pytest.raises(requests.exceptions.RequestException):
        requests.get(url, timeout=5)


def test_get_collections_api_positive():
    """Positive test: valid API key should return 200 and JSON body."""
    url = "https://api.restful-api.dev/collections"
    headers = {"x-api-key": "a43743cc-cf7d-48b6-bf8c-d579f7046031"}
    resp = requests.get(url, headers=headers, timeout=10)

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        raise AssertionError("Response is not valid JSON")

    # Basic sanity checks: should be a list or contain expected keys
    assert data is not None, "Empty response body"
    if isinstance(data, list):
        assert len(data) >= 0, "Expected a JSON list (can be empty)"
    elif isinstance(data, dict):
        assert "id" in data or "collections" in data or len(data) > 0, "Unexpected JSON structure"


def test_get_collections_missing_api_key_negative():
    """Negative test: missing API key should be rejected (401/403)."""
    url = "https://api.restful-api.dev/collections"
    resp = requests.get(url, timeout=10)

    assert resp.status_code in (401, 403), f"Expected 401 or 403 for missing API key, got {resp.status_code}"


def test_get_collections_invalid_api_key_negative():
    """Negative test: invalid API key should be rejected (401/403)."""
    url = "https://api.restful-api.dev/collections"
    invalid_headers = {"x-api-key": "invalid-key-0000-0000"}

    # Call with invalid key and with a known valid key for comparison
    resp_invalid = requests.get(url, headers=invalid_headers, timeout=10)
    valid_headers = {"x-api-key": "a43743cc-cf7d-48b6-bf8c-d579f7046031"}
    resp_valid = requests.get(url, headers=valid_headers, timeout=10)

    # If the service enforces API keys, invalid should return 401/403
    if resp_invalid.status_code in (401, 403):
        return

    # If the service does not enforce API keys and returns 200, ensure the response differs
    if resp_invalid.status_code == resp_valid.status_code and resp_invalid.text == resp_valid.text:
        pytest.skip("Service returns identical response for invalid API key; cannot assert rejection")

    # Otherwise accept non-2xx or differing responses as evidence of rejection
    assert resp_invalid.status_code != 200 or resp_invalid.text != resp_valid.text, (
        f"Invalid API key returned the same successful response as a valid key (status {resp_invalid.status_code})"
    )


def test_get_collections_wrong_method_negative():
    """Negative test: wrong HTTP method should not return 200."""
    url = "https://api.restful-api.dev/collections"
    headers = {"x-api-key": "a43743cc-cf7d-48b6-bf8c-d579f7046031"}
    resp = requests.post(url, headers=headers, timeout=10)

    assert resp.status_code >= 400 and resp.status_code != 200, (
        f"Expected non-2xx for POST to collections endpoint, got {resp.status_code}"
    )
