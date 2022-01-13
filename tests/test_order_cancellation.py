from duffel_api.models import OrderCancellation

from .fixtures import raw_fixture


def test_order_cancellation_model_parsing():
    name = "get-order-cancellation-by-id"
    with raw_fixture(name) as fixture:
        assert OrderCancellation.from_json(fixture["data"])
