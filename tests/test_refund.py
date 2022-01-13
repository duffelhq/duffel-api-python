from duffel_api.models import Refund

from .fixtures import raw_fixture


def test_refund_model_parsing():
    name = "get-refund-by-id"
    with raw_fixture(name) as fixture:
        assert Refund.from_json(fixture["data"])
