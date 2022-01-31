from duffel_api.models import Payment


def test_payment_model_parsing():
    json = {
        "type": "balance",
        "live_mode": False,
        "id": "pay_00009hthhsUZ8W4LxQgkjo",
        "currency": "GBP",
        "created_at": "2020-04-11T15:48:11.642Z",
        "amount": "30.20",
    }
    assert Payment.from_json(json)
