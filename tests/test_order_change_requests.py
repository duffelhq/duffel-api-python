from datetime import datetime, date

from .fixtures import fixture


def test_create_order_change_request(requests_mock):
    url = "air/order_change_requests"
    with fixture("create-order-change-request", url, requests_mock.post, 201) as client:
        slices = {
            "add": [
                {
                    "cabin_class": "economy",
                    "departure_date": "2020-04-24",
                    "destination": "JFK",
                    "origin": "LHR",
                }
            ],
            "remove": [{"slice_id": "sli_00009htYpSCXrwaB9Dn123"}],
        }
        creation = client.order_change_requests.create("order-id").slices(slices)
        change_request = creation.execute()
        assert change_request.created_at == datetime(2020, 1, 17, 10, 12, 14, 545000)

        assert change_request.id == "ocr_0000A3bQP9RLVfNUcdpLpw"
        assert change_request.live_mode is True
        assert change_request.order_id == "ord_0000A3bQ8FJIQoEfuC07n6"
        assert isinstance(change_request.slices.add, type([]))
        assert change_request.slices.add[0].cabin_class == "economy"
        assert change_request.slices.add[0].departure_date == date(2020, 4, 24)
        assert change_request.slices.add[0].destination == "JFK"
        assert change_request.slices.add[0].origin == "LHR"
        assert isinstance(change_request.slices.remove, type([]))
        assert change_request.slices.remove[0].slice_id == "sli_00009htYpSCXrwaB9Dn123"
        assert change_request.updated_at == datetime(2020, 1, 17, 10, 12, 14, 545000)


def test_get_order_change_request(requests_mock):
    url = "air/order_change_requests/order-id"
    with fixture(
        "get-order-change-request-by-id", url, requests_mock.get, 200
    ) as client:
        change_request = client.order_change_requests.get("order-id")
        assert change_request.created_at == datetime(2020, 1, 17, 10, 12, 11, 634000)
        assert change_request.id == "ocr_0000A3bQP9RLVfNUcdpLpw"
        assert change_request.live_mode is True
        assert change_request.order_id == "ord_0000A3bQ8FJIQoEfuC07n6"
        assert isinstance(change_request.order_change_offers, type([]))
        assert (
            change_request.order_change_offers[0].slices.add[0].id
            == "sli_00009htYpSCXrwaB9Dn123"
        )
        assert isinstance(change_request.order_change_offers[0].slices.remove, type([]))
        assert (
            change_request.order_change_offers[0].slices.remove[0].id
            == "sli_00009htYpSCXrwaB9Dn123"
        )
        assert change_request.order_change_offers[0].updated_at == datetime(
            2020, 1, 17, 10, 12, 14, 545000
        )
        assert isinstance(change_request.slices.add, type([]))
        assert change_request.slices.add[0].cabin_class == "economy"
        assert change_request.slices.add[0].departure_date == date(2020, 4, 24)
        assert change_request.slices.add[0].destination == "JFK"
        assert change_request.slices.add[0].origin == "LHR"
        assert isinstance(change_request.slices.remove, type([]))
        assert change_request.slices.remove[0].slice_id == "sli_00009htYpSCXrwaB9Dn123"
        assert change_request.updated_at == datetime(2020, 1, 17, 10, 12, 11, 634000)
