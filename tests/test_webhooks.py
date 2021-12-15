from .fixtures import fixture


def test_create_webhook(requests_mock):
    url = "air/webhooks"
    with fixture("create-webhook", url, requests_mock.post, 201) as client:
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
    url = "air/webhooks/some-id"
    with fixture("update-webhook", url, requests_mock.patch, 200) as client:
        webhook = client.webhooks.update("some-id").active(False).execute()

        assert webhook.id == "sev_0000A3tQSmKyqOrcySrGbo"
        assert not webhook.active
        assert webhook.events == ["order.created", "order.updated"]
        assert webhook.url == "https://www.example.com:4000/webhooks"


def test_ping_webhook(requests_mock):
    url = "air/webhooks/some-id/actions/ping"
    with fixture(
        "ping-webhook", url, requests_mock.post, 204, with_response=False
    ) as client:
        webhook = client.webhooks.ping("some-id")

        assert webhook is None
