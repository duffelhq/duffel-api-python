from .fixtures import fixture


def test_get_seat_maps(requests_mock):
    with fixture(
        "get-seat-maps", "air/seat_maps?offer_id=offer-id", requests_mock.get
    ) as client:
        seat_maps = client.seat_maps.get("offer-id")
        assert len(seat_maps) == 1
        seat_map = seat_maps[0]
        assert len(seat_map.cabins) == 1
        assert seat_map.cabins[0].aisles == 2
        assert len(seat_map.cabins[0].rows) == 7
        element = seat_map.cabins[0].rows[0].sections[0].elements[0]
        assert element.designator == "1A"
        assert element.type == "seat"
        assert element.available_services[0].id == "ase_00009UhD4ongolulWAAA1A"
        assert element.available_services[0].total_amount == "30.00"
