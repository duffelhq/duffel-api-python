import pytest

from duffel_api import Duffel
from duffel_api.api import LinksSessionCreate


def test_create_links_session(requests_mock):
    expected_response = {"data": {"url": "https://links.duffel.com?token=some-token"}}
    requests_mock.post(
        "http://someaddress/links/sessions", json=expected_response, status_code=201
    )
    client = Duffel(access_token="some_token", api_url="http://someaddress")
    response = (
        client.sessions.create()
        .reference("some-reference")
        .success_url("http://some-url")
        .failure_url("http://some-url")
        .abandonment_url("http://some-url")
        .markup_currency("USD")
        .markup_amount("123")
        .execute()
    )
    assert response.url == expected_response["data"]["url"]


def test_create_links_session_with_invalid_data(requests_mock):
    requests_mock.post(
        "http://someaddress/links/sessions",
        json={"data": {"url": "doesnt-matter"}},
        status_code=201,
    )
    client = Duffel(access_token="some_token", api_url="http://someaddress")
    creation = client.sessions.create()

    with pytest.raises(LinksSessionCreate.InvalidMandatoryFields):
        creation.execute()

    creation = (
        creation.reference("some-reference")
        .success_url("http://some-url")
        .failure_url("http://some-url")
        .abandonment_url("http://some-url")
    )

    with pytest.raises(LinksSessionCreate.InvalidMarkup):
        creation.markup_currency("USD").execute()

    # Override this so that the next one also fails
    creation._markup_currency = None
    with pytest.raises(LinksSessionCreate.InvalidMarkup):
        creation.markup_amount("123").execute()
