from duffel_api.models import Offer

from .fixtures import raw_fixture


def test_offer_model_parsing():
    name = "get-offer-by-id"
    with raw_fixture(name) as fixture:
        assert Offer(fixture["data"])
