from duffel_api.models import OrderChangeRequest

from .fixtures import raw_fixture


def test_order_change_request_model_parsing():
    name = "get-order-change-request-by-id"
    with raw_fixture(name) as fixture:
        assert OrderChangeRequest.from_json(fixture["data"])
