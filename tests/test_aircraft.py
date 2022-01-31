from duffel_api.models import Aircraft

from .fixtures import raw_fixture


def test_aircraft_model_parsing():
    name = "get-aircraft-by-id"
    with raw_fixture(name) as fixture:
        assert Aircraft.from_json(fixture["data"])
