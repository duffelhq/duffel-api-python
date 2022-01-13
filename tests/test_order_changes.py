import datetime

import pytest

from duffel_api.api import OrderChangeClient

from .fixtures import fixture


def test_get_order_change_by_id(requests_mock):
    url = "air/order_changes/ocr_0000A3tQSmKyqOrcySrGbo"
    with fixture("get-order-change-by-id", url, requests_mock.get, 200) as client:
        order_change = client.order_changes.get("ocr_0000A3tQSmKyqOrcySrGbo")

        assert order_change.id == "ocr_0000A3tQSmKyqOrcySrGbo"
        assert order_change.change_total_amount == "30.50"
        assert order_change.change_total_currency == "GBP"
        assert order_change.confirmed_at == datetime.datetime(2020, 1, 17, 11, 51, 43)
        assert order_change.created_at == datetime.datetime(
            2020, 4, 11, 15, 48, 11, 642000
        )
        assert order_change.expires_at == datetime.datetime(
            2020, 1, 17, 10, 42, 14, 545052
        )
        assert order_change.new_total_amount == "121.30"
        assert order_change.new_total_currency == "GBP"
        assert order_change.penalty_total_amount == "15.50"
        assert order_change.penalty_total_currency == "GBP"
        assert order_change.refund_to == "voucher"
        assert order_change.order_id == "ord_0000A3tQcCRZ9R8OY0QlxA"
        assert isinstance(order_change.slices.add, type([]))
        assert isinstance(order_change.slices.remove, type([]))
        assert order_change.slices.add[0].id == "sli_00009htYpSCXrwaB9Dn123"
        assert order_change.slices.remove[0].id == "sli_00009htYpSCXrwaB9Dn123"


def test_create_order_change(requests_mock):
    url = "air/order_changes"
    with fixture("create-order-change", url, requests_mock.post, 201) as client:
        order_change = client.order_changes.create("ord_0000A3tQcCRZ9R8OY0QlxA")

        assert order_change.id == "ocr_0000A3tQSmKyqOrcySrGbo"
        assert order_change.order_id == "ord_0000A3tQcCRZ9R8OY0QlxA"
        assert order_change.confirmed_at is None
        assert order_change.refund_to is None


def test_confirm_order_change(requests_mock):
    url = "air/order_changes/ocr_0000A3tQSmKyqOrcySrGbo/actions/confirm"
    with fixture("confirm-order-change", url, requests_mock.post, 200) as client:
        payment = {"type": "balance", "currency": "GBP", "amount": "30.20"}

        order_change = client.order_changes.confirm(
            "ocr_0000A3tQSmKyqOrcySrGbo", payment
        )

        assert order_change.id == "ocr_0000A3tQSmKyqOrcySrGbo"
        assert order_change.order_id == "ord_0000A3tQcCRZ9R8OY0QlxA"
        assert order_change.confirmed_at == datetime.datetime(2020, 1, 17, 11, 51, 43)
        assert order_change.refund_to == "voucher"


def test_confirm_order_change_with_invalid_data(requests_mock):
    url = "air/order_changes/ocr_0000A3tQSmKyqOrcySrGbo/actions/confirm"
    with fixture("confirm-order-change", url, requests_mock.post, 200) as client:
        with pytest.raises(OrderChangeClient.InvalidPayment):
            client.order_changes.confirm(
                "ocr_0000A3tQSmKyqOrcySrGbo", {"type": "balance", "currency": "GBP"}
            )

        with pytest.raises(OrderChangeClient.InvalidPaymentType):
            client.order_changes.confirm(
                "ocr_0000A3tQSmKyqOrcySrGbo",
                {"type": "unknown", "currency": "GBP", "amount": "30.20"},
            )
