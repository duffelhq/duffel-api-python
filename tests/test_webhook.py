from duffel_api.models import Webhook


def test_webhook_model_parsing():
    json = {
        "url": "https://www.example.com:4000/webhooks",
        "updated_at": "2020-04-11T15:48:11.642Z",
        "secret": "QKfUULLQh+8SegYmIsF6kA==",
        "live_mode": "true",
        "id": "sev_0000A3tQSmKyqOrcySrGbo",
        "events": ["order.created", "order.updated"],
        "created_at": "2020-04-11T15:48:11.642Z",
        "active": "true",
    }
    assert Webhook.from_json(json)
