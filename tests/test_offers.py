import pytest
from .fixtures import fixture

from duffel_api.api import OfferClient


def test_get_offer_by_id(requests_mock):
    url = "air/offers/id"
    with fixture("get-offer-by-id", url, requests_mock.get, 200) as client:
        offer = client.offers.get("id")
        assert offer.id == "off_00009htYpSCXrwaB9DnUm0"
        assert len(offer.slices) == 1
        assert offer.owner.id == "aln_00001876aqC8c5umZmrRds"
        assert offer.owner.name == "British Airways"
        assert len(offer.passengers) == 1
        assert len(offer.available_services) == 1
        service = offer.available_services[0]
        assert service.type == "baggage"
        assert service.total_amount == "15.00"
        assert service.total_currency == "GBP"


def test_get_offers(requests_mock):
    # We need a way to ensure pagination finished in a mocking environment
    end_pagination_url = (
        "http://someaddress/air/offers?limit=50"
        + "&offer_request_id=offer_request_id"
        + "&after=g2wAAAACbQAAABBBZXJvbWlzdC1LaGFya2l2bQAAAB%3D"
    )
    end_pagination_response = {"meta": {"after": None}, "data": []}
    requests_mock.get(
        end_pagination_url, complete_qs=True, json=end_pagination_response
    )

    url = "air/offers?limit=50&offer_request_id=offer_request_id"
    with fixture("get-offers", url, requests_mock.get, 200) as client:
        paginated_offers = client.offers.list("offer_request_id")
        offers = list(paginated_offers)
        assert len(offers) == 1
        offer = offers[0]
        assert offer.id == "off_00009htYpSCXrwaB9DnUm0"
        assert len(offer.slices) == 2
        slice_1 = offer.slices[0]
        assert slice_1.conditions.change_before_departure.allowed is True
        assert slice_1.conditions.change_before_departure.penalty_amount == "100.00"
        assert slice_1.conditions.change_before_departure.penalty_currency == "GBP"
        assert len(slice_1.segments) == 1
        assert slice_1.segments[0].id == "seg_00009htYpSCXrwaB9Dn456"
        slice_2 = offer.slices[1]
        assert slice_2.conditions.change_before_departure is None
        assert len(slice_2.segments) == 1
        assert slice_2.segments[0].id == "seg_0000AEfTff29Oo8LXf7FYG"


def test_offer_update_passenger(requests_mock):
    offer_id = "off_00009htYpSCXrwaB9DnUm0"
    offer_passenger_id = "pas_00009hj8USM7Ncg31cBCL"

    url = f"air/offers/{offer_id}/passengers/{offer_passenger_id}"

    with fixture(
        "update-offer-passenger-by-id", url, requests_mock.patch, 200
    ) as client:
        offer_passenger = client.offers.update_passenger(
            offer_id,
            offer_passenger_id,
            "Earhart",
            "Amelia",
            [{"account_number": "12901014", "airline_iata_code": "BA"}],
        )

        assert offer_passenger.id == offer_passenger_id
        assert offer_passenger.family_name == "Earhart"
        assert offer_passenger.given_name == "Amelia"
        assert (
            offer_passenger.loyalty_programme_accounts[0].account_number == "12901014"
        )
        assert offer_passenger.loyalty_programme_accounts[0].airline_iata_code == "BA"


def test_offer_update_passenger_with_invalid_data(requests_mock):
    offer_id = "off_00009htYpSCXrwaB9DnUm0"
    offer_passenger_id = "pas_00009hj8USM7Ncg31cBCL"

    url = f"air/offers/{offer_id}/passengers/{offer_passenger_id}"

    with fixture(
        "update-offer-passenger-by-id", url, requests_mock.patch, 200
    ) as client:
        with pytest.raises(OfferClient.InvalidOfferId):
            client.offers.update_passenger(
                "",
                offer_passenger_id,
                "Earhart",
                "Amelia",
                [{"account_number": "12901014", "airline_iata_code": "BA"}],
            )

        with pytest.raises(OfferClient.InvalidOfferPassengerId):
            client.offers.update_passenger(
                offer_id,
                "",
                "Earhart",
                "Amelia",
                [{"account_number": "12901014", "airline_iata_code": "BA"}],
            )

        with pytest.raises(OfferClient.InvalidFamilyName):
            client.offers.update_passenger(
                offer_id,
                offer_passenger_id,
                "",
                "Amelia",
                [{"account_number": "12901014", "airline_iata_code": "BA"}],
            )

        with pytest.raises(OfferClient.InvalidGivenName):
            client.offers.update_passenger(
                offer_id,
                offer_passenger_id,
                "Earhart",
                "",
                [{"account_number": "12901014", "airline_iata_code": "BA"}],
            )

        with pytest.raises(OfferClient.InvalidLoyaltyProgrammeAirlineIataCode):
            client.offers.update_passenger(
                offer_id,
                offer_passenger_id,
                "Earhart",
                "Amelia",
                [{"account_number": "12901014", "airline_iata_code": ""}],
            )

        with pytest.raises(OfferClient.InvalidLoyaltyProgrammeAccountNumber):
            client.offers.update_passenger(
                offer_id,
                offer_passenger_id,
                "Earhart",
                "Amelia",
                [{"account_number": "", "airline_iata_code": "BA"}],
            )
