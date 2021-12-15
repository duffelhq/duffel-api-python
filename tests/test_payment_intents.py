import pytest

from duffel_api.api import PaymentIntentCreate

from .fixtures import fixture


def test_create_payment_intent(requests_mock):
    url = "payments/payment_intents"
    with fixture("create-payment-intent", url, requests_mock.post) as client:
        payment_intent_details = {
            "amount": "30.20",
            "currency": "GBP",
        }
        creation = client.payment_intents.create()
        payment_intent = creation.payment(payment_intent_details).execute()

        assert payment_intent.id == "pit_0000AEQIx7Swvd9nmMNGkq"
        assert payment_intent.status == "requires_payment_method"
        assert payment_intent.amount == "30.20"
        assert payment_intent.currency == "GBP"


def test_create_payment_intent_with_invalid_data(requests_mock):
    url = "payments/payment_intents"
    with fixture("create-payment-intent", url, requests_mock.post) as client:
        creation = client.payment_intents.create()
        with pytest.raises(PaymentIntentCreate.InvalidPayment):
            creation.payment({})

        with pytest.raises(PaymentIntentCreate.InvalidPayment):
            creation.payment({"amount": "100.00"})

        with pytest.raises(PaymentIntentCreate.InvalidPayment):
            creation.payment({"currency": "AUD"})
