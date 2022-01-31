from duffel_api.models import Airport

from .fixtures import raw_fixture


def test_airport_model_parsing():
    name = "get-airport-by-id"
    with raw_fixture(name) as fixture:
        assert Airport.from_json(fixture["data"])
