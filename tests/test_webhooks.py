import pytest

from .fixtures import fixture


def test_create_webhook(requests_mock):
    with fixture("create-webhook", "air/webhooks", requests_mock.post) as client:
        webhook = (
            client.webhooks.create()
            .url("https://www.example.com:4000/webhooks")
            .events(["order.created", "order.updated"])
            .execute()
        )

        assert webhook.id == "sev_0000A3tQSmKyqOrcySrGbo"
        assert webhook.active
        assert webhook.events == ["order.created", "order.updated"]
        assert webhook.secret == "QKfUULLQh+8SegYmIsF6kA=="
        assert webhook.url == "https://www.example.com:4000/webhooks"


def test_update_webhook(requests_mock):
    with fixture(
        "update-webhook", "air/webhooks/some-id", requests_mock.patch
    ) as client:
        webhook = client.webhooks.update("some-id").active(False).execute()

        assert webhook.id == "sev_0000A3tQSmKyqOrcySrGbo"
        assert not webhook.active
        assert webhook.events == ["order.created", "order.updated"]
        assert webhook.url == "https://www.example.com:4000/webhooks"


@pytest.mark.skip(
    reason="""Webhook#Ping does not return a body. Our current tests do not look
    at status codes, so there isn't anything in particular to test here."""
)
def test_ping_webhook(requests_mock):
    url = "air/webhooks/some-id/actions/ping"
    with fixture("ping-webhook", url, requests_mock.post) as client:
        webhook = client.webhooks.ping("some-id")

        assert webhook is None
