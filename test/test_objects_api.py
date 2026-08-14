import os
import requests
import pytest

BASE = os.environ.get("API_BASE", "https://api.restful-api.dev/objects")
TIMEOUT = 10


def get_object(obj_id):
    url = f"{BASE}/{obj_id}"
    return requests.get(url, timeout=TIMEOUT)


def find_existing_id():
    resp = requests.get(BASE, timeout=TIMEOUT)
    if resp.status_code != 200:
        return None
    try:
        data = resp.json()
    except ValueError:
        return None

    # If the API returns a list of objects, try to extract an id
    if isinstance(data, list) and len(data) > 0:
        first = data[0]
        if isinstance(first, dict) and "id" in first:
            return str(first["id"])
    # If it returns a dict with an id key
    if isinstance(data, dict) and "id" in data:
        return str(data["id"])

    # Fallback: common working id used elsewhere in this repo
    return "13"


def test_get_object_positive_existing_id():
    """Positive: GET an existing object id returns 200 and JSON."""
    obj_id = find_existing_id()
    if not obj_id:
        pytest.skip("Could not discover an existing object id from the list endpoint")

    resp = get_object(obj_id)
    assert resp.status_code == 200, f"Expected 200 for id {obj_id}, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response was not valid JSON")

    if isinstance(data, dict) and "id" in data:
        assert str(data["id"]) == str(obj_id), f"Expected id {obj_id}, got {data.get('id')}"


@pytest.mark.parametrize("bad_id", ["999999999", "nonexistent-id-xyz", "abc!@#"], ids=["large-num", "random-uuid-like", "malformed"]) 
def test_get_object_negative_not_found_or_bad_request(bad_id):
    """Negative: non-existent or malformed ids should not return 200."""
    resp = get_object(bad_id)
    # Accept any 4xx/5xx as evidence of rejection/not found
    assert resp.status_code >= 400 and resp.status_code != 200, (
        f"Expected non-2xx for bad id '{bad_id}', got {resp.status_code}"
    )


@pytest.mark.parametrize("edge_id", [str(2**63), "..%2F..%2Fetc%2Fpasswd", "\u2603", ""]) 
def test_get_object_edge_cases(edge_id):
    """Edge: very large numbers, path-traversal-like, unicode, and empty id handling."""
    # For empty id, call the collection endpoint instead
    if edge_id == "":
        resp = requests.get(BASE, timeout=TIMEOUT)
        # Collection endpoint should be 200 (list) or similar; assert not server error
        assert resp.status_code < 500, f"Unexpected server error for collection endpoint: {resp.status_code}"
        return

    resp = get_object(edge_id)
    # Expect safe behavior: either handled as not found/bad request or rejected
    assert resp.status_code >= 400 and resp.status_code != 200, (
        f"Edge id '{edge_id}' unexpectedly returned {resp.status_code}"
    )


if __name__ == "__main__":
    # Quick runner
    test_get_object_positive_existing_id()
    test_get_object_negative_not_found_or_bad_request("999999999")
    test_get_object_edge_cases("..%2F..%2Fetc%2Fpasswd")
