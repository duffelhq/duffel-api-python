from duffel_api.models import Airline

from .fixtures import raw_fixture


def test_airline_model_parsing():
    name = "get-airline-by-id"
    with raw_fixture(name) as fixture:
        assert Airline.from_json(fixture["data"])
