from duffel_api.models import OrderChangeOffer

from .fixtures import raw_fixture


def test_order_change_offer_model_parsing():
    name = "get-order-change-offer-by-id"
    with raw_fixture(name) as fixture:
        assert OrderChangeOffer.from_json(fixture["data"])
