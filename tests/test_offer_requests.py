import pytest

from duffel_api.api import OfferRequestCreate

from .fixtures import fixture


def test_get_offer_request_by_id(requests_mock):
    url = "air/offer_requests/id"
    with fixture("get-offer-request-by-id", url, requests_mock.get, 200) as client:
        offer_request = client.offer_requests.get("id")
        assert offer_request.id == "orq_00009hjdomFOCJyxHG7k7k"
        assert len(offer_request.slices) == 1
        assert len(offer_request.passengers) == 1
        slice = offer_request.slices[0]
        assert slice.origin_type == "airport"


def test_get_offer_requests(requests_mock):
    # We need a way to ensure pagination finished in a mocking environment
    end_pagination_url = (
        "http://someaddress/air/offer_requests?limit=50"
        + "&after=g2wAAAACbQAAABBBZXJvbWlzdC1LaGFya2l2bQAAAB%3D"
    )
    end_pagination_response = {"meta": {"after": None}, "data": []}
    requests_mock.get(
        end_pagination_url, complete_qs=True, json=end_pagination_response
    )

    url = "air/offer_requests?limit=50"
    with fixture("get-offer-requests", url, requests_mock.get, 200) as client:
        paginated_offer_requests = client.offer_requests.list()
        offer_requests = list(paginated_offer_requests)
        assert len(offer_requests) == 1
        offer_request = offer_requests[0]
        assert offer_request.id == "orq_00009hjdomFOCJyxHG7k7k"


def test_create_offer_request(requests_mock):
    url = "air/offer_requests?return_offers=false"
    with fixture("create-offer-request", url, requests_mock.post, 201) as client:
        passengers = [{"type": "adult"}]
        slices = [
            {
                "departure_date": "2100-02-27",
                "destination": "LGW",
                "origin": "LIS",
            }
        ]
        offer_request = (
            client.offer_requests.create()
            .passengers(passengers)
            .slices(slices)
            .execute()
        )
        assert offer_request.id == "orq_00009hjdomFOCJyxHG7k7k"
        assert len(offer_request.offers) == 1
        offer = offer_request.offers[0]
        assert offer.id == "off_00009htYpSCXrwaB9DnUm0"


def test_create_offer_request_with_invalid_data(requests_mock):
    url = "air/offer_requests?return_offers=false"
    with fixture("create-offer-request", url, requests_mock.post, 422) as client:
        creation = client.offer_requests.create()
        with pytest.raises(OfferRequestCreate.InvalidNumberOfPassengers):
            creation.execute()

        with pytest.raises(OfferRequestCreate.InvalidPassenger):
            creation.passengers([{}]).execute()

        with pytest.raises(OfferRequestCreate.InvalidCabinClass):
            creation.cabin_class("invalid").execute()

        passengers = [{"type": "adult"}]

        creation = creation.passengers(passengers)
        with pytest.raises(OfferRequestCreate.InvalidNumberOfSlices):
            creation.execute()
        with pytest.raises(OfferRequestCreate.InvalidSlice):
            creation.slices([{}]).execute()
