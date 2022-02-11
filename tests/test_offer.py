from duffel_api.models import Offer

from .fixtures import raw_fixture


def test_offer_model_parsing():
    name = "get-offer-by-id"
    with raw_fixture(name) as fixture:
        assert Offer.from_json(fixture["data"])


def test_offer_model_parsing_with_nullable_payment_requirements():
    name = "get-offer-by-id-with-null-payment-requirements"
    with raw_fixture(name) as fixture:
        assert Offer.from_json(fixture["data"])
