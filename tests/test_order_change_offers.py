import datetime

from .fixtures import fixture


def test_get_order_change_offer_by_id(requests_mock):
    url = "air/order_change_offers/id"
    with fixture("get-order-change-offer-by-id", url, requests_mock.get, 200) as client:
        order_change_offer = client.order_change_offers.get("id")

        assert order_change_offer.id == "oco_0000A3vUda8dKRtUSQPSXw"
        assert order_change_offer.change_total_amount == "90.80"
        assert order_change_offer.change_total_currency == "GBP"
        assert order_change_offer.created_at == datetime.datetime(
            2020, 1, 17, 10, 12, 14, 545000
        )
        assert order_change_offer.expires_at == datetime.datetime(
            2020, 1, 17, 10, 42, 14
        )
        assert order_change_offer.new_total_amount == "35.50"
        assert order_change_offer.new_total_currency == "GBP"
        assert order_change_offer.order_change_id == "oce_0000A4QasEUIjJ6jHKfhHU"
        assert order_change_offer.penalty_amount == "10.50"
        assert order_change_offer.penalty_currency == "GBP"
        assert order_change_offer.refund_to == "arc_bsp_cash"
        assert order_change_offer.updated_at == datetime.datetime(
            2020, 1, 17, 10, 12, 14, 545000
        )
        assert isinstance(order_change_offer.slices.add, type([]))
        assert isinstance(order_change_offer.slices.remove, type([]))
        order_change_offer.slices.add[0].id == "sli_00009htYpSCXrwaB9Dn123"
        order_change_offer.slices.remove[0].id == "sli_00009htYpSCXrwaB9Dn123"


def test_get_order_change_offers(requests_mock):
    # We need a way to ensure pagination finished in a mocking environment
    end_pagination_url = (
        "http://someaddress/air/order_change_offers?limit=50"
        + "&order_change_request_id=ocr_0000A3bQP9RLVfNUcdpLpw"
        + "&after=g2wAAAACbQAAABBBZXJvbWlzdC1LaGFya2l2bQAAAB%3D"
    )
    end_pagination_response = {"meta": {"after": None}, "data": []}
    requests_mock.get(
        end_pagination_url, complete_qs=True, json=end_pagination_response
    )

    url = (
        "air/order_change_offers?limit=50"
        + "&order_change_request_id=ocr_0000A3bQP9RLVfNUcdpLpw"
    )
    with fixture(
        "get-order-change-offers-by-order-change-request-id",
        url,
        requests_mock.get,
        200,
    ) as client:
        paginated_order_change_offers = client.order_change_offers.list(
            "ocr_0000A3bQP9RLVfNUcdpLpw"
        )
        order_change_offers = list(paginated_order_change_offers)
        assert len(order_change_offers) == 1
        offer = order_change_offers[0]
        assert offer.id == "oco_0000A3vUda8dKRtUSQPSXw"
        assert offer.refund_to == "original_form_of_payment"
