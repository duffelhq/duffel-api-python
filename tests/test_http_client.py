import pytest

from duffel_api.http_client import HttpClient, ApiError


def test_http_client(requests_mock):
    requests_mock.get("http://someaddress/api/stuff", json={})
    client = HttpClient("some_token", "http://someaddress", "v1")
    assert client.do_get("/api/stuff") == {}


def test_http_client_error(requests_mock):
    error = {
        "meta": {"status": 500, "request_id": "FmXeZifDA60QOlgAAODB"},
        "errors": [
            {
                "type": "airline_error",
                "title": "Unexpected Airline Error",
                "source": "iberia",
                "message": "The airline responded with an unexpected error.",
                "documentation_url": "https://duffel.com/docs/api/overview/errors",
                "code": "airline_unknown",
            }
        ],
    }
    requests_mock.get("http://someaddress/api/stuff", json=error, status_code=500)
    client = HttpClient("some_token", "http://someaddress", "v1")
    with pytest.raises(
        ApiError, match="The airline responded with an unexpected error"
    ) as excinfo:
        client.do_get("/api/stuff")
    assert excinfo.value.meta["request_id"] == "FmXeZifDA60QOlgAAODB"
