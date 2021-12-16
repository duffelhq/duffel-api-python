import pytest

from datetime import datetime

from duffel_api.api import PaymentIntentCreate

from .fixtures import fixture


def test_create_payment_intent(requests_mock):
    url = "payments/payment_intents"
    with fixture("create-payment-intent", url, requests_mock.post, 201) as client:
        payment_intent_details = {
            "amount": "30.20",
            "currency": "GBP",
        }
        creation = client.payment_intents.create()
        payment_intent = creation.payment(payment_intent_details).execute()

        assert payment_intent.amount == "30.20"
        assert (
            payment_intent.client_token
            == "eyJjbGllbnRfc2VjcmV0IjoicGlfM0s2dFMyQW5rMVRkeXJvRDA0eVVzM1BxX3NlY3JldF9VY"
            + "zV3VjRYU0hUc2VHWHlSOHhpTTNsdFdjIiwicHVibGlzaGFibGVfa2V5IjoicGtfdGVzdF81MUl"
            + "0Q3YwQW5rMVRkeXJvRGxFTGExeGdZZkpBMUdUdzh2VmRRVmVRUEl3S1hiVjk5MVNnNnJpY1Nac"
            + "1hJWGtTZ2VGWGF1c1RBcVVQSkhUNXNMZWpIdFlIUjAwVEVESVh4cnMifQ=="
        )
        assert payment_intent.confirmed_at is None
        assert payment_intent.created_at == datetime(2020, 4, 11, 15, 48, 11, 642000)
        assert payment_intent.currency == "GBP"
        assert payment_intent.fees_amount is None
        assert payment_intent.fees_currency is None
        assert payment_intent.id == "pit_0000AEQIx7Swvd9nmMNGkq"
        assert payment_intent.live_mode is True
        assert payment_intent.net_amount is None
        assert payment_intent.net_currency is None
        assert payment_intent.refunds == []
        assert payment_intent.status == "requires_payment_method"
        assert payment_intent.updated_at == datetime(2020, 4, 11, 15, 48, 11, 642000)


def test_create_payment_intent_with_invalid_data(requests_mock):
    url = "payments/payment_intents"
    with fixture("create-payment-intent", url, requests_mock.post, 422) as client:
        creation = client.payment_intents.create()
        with pytest.raises(PaymentIntentCreate.InvalidPayment):
            creation.payment({})

        with pytest.raises(PaymentIntentCreate.InvalidPayment):
            creation.payment({"amount": "100.00"})

        with pytest.raises(PaymentIntentCreate.InvalidPayment):
            creation.payment({"currency": "AUD"})


def test_get_payment_intent(requests_mock):
    url = "payments/payment_intents/id"
    with fixture("get-payment-intent-by-id", url, requests_mock.get, 200) as client:
        payment_intent = client.payment_intents.get("id")

        assert payment_intent.amount == "30.20"
        assert (
            payment_intent.client_token
            == "eyJjbGllbnRfc2VjcmV0IjoicGlfM0s2dFMyQW5rMVRkeXJvRDA0eVVzM1BxX3NlY3JldF9VY"
            + "zV3VjRYU0hUc2VHWHlSOHhpTTNsdFdjIiwicHVibGlzaGFibGVfa2V5IjoicGtfdGVzdF81MUl"
            + "0Q3YwQW5rMVRkeXJvRGxFTGExeGdZZkpBMUdUdzh2VmRRVmVRUEl3S1hiVjk5MVNnNnJpY1Nac"
            + "1hJWGtTZ2VGWGF1c1RBcVVQSkhUNXNMZWpIdFlIUjAwVEVESVh4cnMifQ=="
        )
        assert payment_intent.confirmed_at is None
        assert payment_intent.card_country_code == "GB"
        assert payment_intent.card_last_four_digits == "0000"
        assert payment_intent.card_network == "visa"
        assert payment_intent.created_at == datetime(2020, 4, 11, 15, 48, 11, 642000)
        assert payment_intent.currency == "GBP"
        assert payment_intent.fees_amount is None
        assert payment_intent.fees_currency is None
        assert payment_intent.id == "pit_0000AEQIx7Swvd9nmMNGkq"
        assert payment_intent.live_mode is True
        assert payment_intent.net_amount is None
        assert payment_intent.net_currency is None
        assert payment_intent.refunds == []
        assert payment_intent.status == "succeeded"
        assert payment_intent.updated_at == datetime(2020, 4, 11, 15, 48, 39, 246000)


def test_confirm_payment_intent(requests_mock):
    url = "payments/payment_intents/id/actions/confirm"
    with fixture("confirm-payment-intent", url, requests_mock.post, 200) as client:
        payment_intent = client.payment_intents.confirm("id")

        assert payment_intent.amount == "30.20"
        assert (
            payment_intent.client_token
            == "eyJjbGllbnRfc2VjcmV0IjoicGlfM0s2dFMyQW5rMVRkeXJvRDA0eVVzM1BxX3NlY3JldF9VY"
            + "zV3VjRYU0hUc2VHWHlSOHhpTTNsdFdjIiwicHVibGlzaGFibGVfa2V5IjoicGtfdGVzdF81MUl"
            + "0Q3YwQW5rMVRkeXJvRGxFTGExeGdZZkpBMUdUdzh2VmRRVmVRUEl3S1hiVjk5MVNnNnJpY1Nac"
            + "1hJWGtTZ2VGWGF1c1RBcVVQSkhUNXNMZWpIdFlIUjAwVEVESVh4cnMifQ=="
        )
        assert payment_intent.confirmed_at == datetime(2020, 4, 11, 15, 48, 30, 321000)
        assert payment_intent.card_country_code == "GB"
        assert payment_intent.card_last_four_digits == "0000"
        assert payment_intent.card_network == "visa"
        assert payment_intent.created_at == datetime(2020, 4, 11, 15, 48, 11, 642000)
        assert payment_intent.currency == "GBP"
        assert payment_intent.fees_amount == "0.42"
        assert payment_intent.fees_currency == "GBP"
        assert payment_intent.id == "pit_0000AEQIx7Swvd9nmMNGkq"
        assert payment_intent.live_mode is True
        assert payment_intent.net_amount == "29.78"
        assert payment_intent.net_currency == "GBP"
        assert payment_intent.refunds == []
        assert payment_intent.status == "succeeded"
        assert payment_intent.updated_at == datetime(2020, 4, 11, 15, 48, 39, 246000)
