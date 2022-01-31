from duffel_api.models import PaymentIntent

from .fixtures import raw_fixture


def test_payment_intent_model_parsing():
    name = "get-payment-intent-by-id"
    with raw_fixture(name) as fixture:
        assert PaymentIntent.from_json(fixture["data"])
