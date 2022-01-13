from duffel_api.models import OrderChange

from .fixtures import raw_fixture


def test_order_change_model_parsing():
    name = "get-order-change-by-id"
    with raw_fixture(name) as fixture:
        assert OrderChange.from_json(fixture["data"])
