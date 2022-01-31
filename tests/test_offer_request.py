from duffel_api.models import OfferRequest

from .fixtures import raw_fixture


def test_offer_request_model_parsing():
    name = "get-offer-request-by-id"
    with raw_fixture(name) as fixture:
        assert OfferRequest.from_json(fixture["data"])
