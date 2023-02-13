import pytest

from duffel_api.api import PartialOfferRequestCreate

from .fixtures import fixture


def test_get_partial_offer_request_by_id(requests_mock):
    url = "air/partial_offer_requests/id"
    with fixture(
        "get-partial-offer-request-by-id", url, requests_mock.get, 200
    ) as client:
        offer_request = client.partial_offer_requests.get("id")
        assert offer_request.id == "orq_00009hjdomFOCJyxHG7k7k"
        assert len(offer_request.slices) == 1
        assert len(offer_request.passengers) == 1
        slice = offer_request.slices[0]
        assert slice.origin_type == "airport"
        assert len(offer_request.offers) == 1
        offer = offer_request.offers[0]
        assert offer.partial
        assert offer.id == "off_00009htYpSCXrwaB9DnUm0"


def test_create_partial_offer_request(requests_mock):
    url = "air/partial_offer_requests"
    with fixture(
        "create-partial-offer-request", url, requests_mock.post, 201
    ) as client:
        passengers = [{"type": "adult"}]
        slices = [
            {
                "departure_date": "2100-02-27",
                "destination": "LGW",
                "origin": "LIS",
            }
        ]
        offer_request = (
            client.partial_offer_requests.create()
            .passengers(passengers)
            .slices(slices)
            .execute()
        )
        assert offer_request.id == "orq_00009hjdomFOCJyxHG7k7k"
        assert len(offer_request.offers) == 1
        offer = offer_request.offers[0]
        assert offer.id == "off_00009htYpSCXrwaB9DnUm0"
        assert offer.partial


def test_get_partial_offer_request_fares_by_id(requests_mock):
    url = "air/partial_offer_requests/id/fares?selected_partial_offer[]=some-partial-offer-id"  # noqa: E501
    with fixture(
        "get-partial-offer-request-by-id", url, requests_mock.get, 200
    ) as client:
        offer_request = client.partial_offer_requests.fares(
            "id", selected_partial_offers=["some-partial-offer-id"]
        )
        assert offer_request.id == "orq_00009hjdomFOCJyxHG7k7k"
        assert len(offer_request.slices) == 1
        assert len(offer_request.passengers) == 1
        slice = offer_request.slices[0]
        assert slice.origin_type == "airport"
        assert len(offer_request.offers) == 1
        offer = offer_request.offers[0]
        assert offer.partial
        assert offer.id == "off_00009htYpSCXrwaB9DnUm0"
        assert offer.tax_amount == "40.80"
        assert offer.total_amount == "45.00"
        assert offer.total_currency == "GBP"


def test_create_partial_offer_request_with_invalid_data(requests_mock):
    url = "air/partial_offer_requests"
    with fixture(
        "create-partial-offer-request", url, requests_mock.post, 422
    ) as client:
        creation = client.partial_offer_requests.create()
        with pytest.raises(PartialOfferRequestCreate.InvalidNumberOfPassengers):
            creation.execute()

        with pytest.raises(PartialOfferRequestCreate.InvalidPassenger):
            creation.passengers([{}]).execute()

        with pytest.raises(PartialOfferRequestCreate.InvalidCabinClass):
            creation.cabin_class("invalid").execute()

        passengers = [{"type": "adult"}]

        creation = creation.passengers(passengers)
        with pytest.raises(PartialOfferRequestCreate.InvalidNumberOfSlices):
            creation.execute()
        with pytest.raises(PartialOfferRequestCreate.InvalidSlice):
            creation.slices([{}]).execute()
