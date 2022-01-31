from duffel_api.models import SeatMap

from .fixtures import raw_fixture


def test_seat_map_model_parsing():
    name = "get-seat-maps"
    with raw_fixture(name) as fixture:
        assert SeatMap.from_json(fixture["data"][0])
