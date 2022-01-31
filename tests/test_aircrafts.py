from .fixtures import fixture


def test_get_aircraft_by_id(requests_mock):
    url = "air/aircraft/id"
    with fixture("get-aircraft-by-id", url, requests_mock.get, 200) as client:
        aircraft = client.aircraft.get("id")
        assert aircraft.id == "arc_00009UhD4ongolulWd91Ky"
        assert aircraft.name == "Airbus Industries A380"
        assert aircraft.iata_code == "380"


def test_get_aircraft(requests_mock):
    # We need a way to ensure pagination finished in a mocking environment
    end_pagination_url = (
        "http://someaddress/air/aircraft?limit=50"
        + "&after=g2wAAAACbQAAABBBZXJvbWlzdC1LaGFya2l2bQAAAB%3D"
    )
    end_pagination_response = {"meta": {"after": None}, "data": []}
    requests_mock.get(
        end_pagination_url, complete_qs=True, json=end_pagination_response
    )

    url = "air/aircraft?limit=50"
    with fixture("get-aircraft", url, requests_mock.get, 200) as client:
        paginated_aircraft = client.aircraft.list()
        aircraft = list(paginated_aircraft)
        assert len(aircraft) == 1
        aircraft = aircraft[0]
        assert aircraft.id == "arc_00009UhD4ongolulWd91Ky"
        assert aircraft.name == "Airbus Industries A380"
        assert aircraft.iata_code == "380"
