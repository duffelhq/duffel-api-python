from .fixtures import fixture


def test_get_airport_by_id(requests_mock):
    url = "air/airports/id"
    with fixture("get-airport-by-id", url, requests_mock.get, 200) as client:
        airport = client.airports.get("id")
        assert airport.id == "arp_lhr_gb"
        assert airport.name == "Heathrow"
        assert airport.iata_code == "LHR"
        assert airport.city.name == "London"


def test_get_airports(requests_mock):
    # We need a way to ensure pagination finished in a mocking environment
    end_pagination_url = (
        "http://someaddress/air/airports?limit=50"
        + "&after=g2wAAAACbQAAABBBZXJvbWlzdC1LaGFya2l2bQAAAB%3D"
    )
    end_pagination_response = {"meta": {"after": None}, "data": []}
    requests_mock.get(
        end_pagination_url, complete_qs=True, json=end_pagination_response
    )

    url = "air/airports?limit=50"
    with fixture("get-airports", url, requests_mock.get, 200) as client:
        paginated_airports = client.airports.list()
        airports = list(paginated_airports)
        assert len(airports) == 1
        airport = airports[0]
        assert airport.id == "arp_lhr_gb"
        assert airport.name == "Heathrow"
        assert airport.iata_code == "LHR"
        assert airport.city.name == "London"
