from .fixtures import fixture


def test_get_offer_by_id(requests_mock):
    with fixture("get-offer-by-id", "air/offers/id", requests_mock.get) as client:
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
    with fixture("get-offers", url, requests_mock.get) as client:
        paginated_offers = client.offers.list("offer_request_id")
        offers = list(paginated_offers)
        assert len(offers) == 1
        offer = offers[0]
        assert offer.id == "off_00009htYpSCXrwaB9DnUm0"
