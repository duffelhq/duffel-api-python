from duffel_api.models import Order

from .fixtures import raw_fixture


def test_order_model_parsing():
    name = "get-order-by-id"
    with raw_fixture(name) as fixture:
        assert Order.from_json(fixture["data"])
