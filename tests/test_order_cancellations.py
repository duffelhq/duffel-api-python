import datetime

from .fixtures import fixture


def test_get_order_cancellation_by_id(requests_mock):
    url = "air/order_cancellations/id"
    with fixture("get-order-cancellation-by-id", url, requests_mock.get, 200) as client:
        order_cancellation = client.order_cancellations.get("id")
        assert order_cancellation.id == "ore_00009qzZWzjDipIkqpaUAj"
        assert order_cancellation.order_id == "ord_00009hthhsUZ8W4LxQgkjo"
        assert order_cancellation.refund_amount == "90.80"
        assert order_cancellation.refund_currency == "GBP"
        assert order_cancellation.refund_to == "arc_bsp_cash"


def test_get_order_cancellations(requests_mock):
    # We need a way to ensure pagination finished in a mocking environment
    end_pagination_url = (
        "http://someaddress/air/order_cancellations?limit=50"
        + "&after=g2wAAAACbQAAABBBZXJvbWlzdC1LaGFya2l2bQAAAB%3D&order_id=order-id"
    )
    end_pagination_response = {"meta": {"after": None}, "data": []}
    requests_mock.get(
        end_pagination_url, complete_qs=True, json=end_pagination_response
    )

    url = "air/order_cancellations?limit=50&order_id=order-id"
    with fixture("get-order-cancellations", url, requests_mock.get, 200) as client:
        paginated_order_cancellations = client.order_cancellations.list("order-id")
        order_cancellations = list(paginated_order_cancellations)
        assert len(order_cancellations) == 1
        order_cancellation = order_cancellations[0]
        assert order_cancellation.id == "ore_00009qzZWzjDipIkqpaUAj"


def test_create_order_cancellation(requests_mock):
    url = "air/order_cancellations"
    with fixture("create-order-cancellation", url, requests_mock.post, 201) as client:
        cancellation = client.order_cancellations.create("order-id")
        assert cancellation.id == "ore_00009qzZWzjDipIkqpaUAj"
        assert cancellation.refund_to == "arc_bsp_cash"
        assert cancellation.refund_currency == "GBP"
        assert cancellation.refund_amount == "90.80"


def test_confirm_order_cancellation(requests_mock):
    url = "air/order_cancellations/some-id/actions/confirm"
    with fixture("confirm-order-cancellation", url, requests_mock.post, 200) as client:
        cancellation = client.order_cancellations.confirm("some-id")
        assert cancellation.id == "ore_00009qzZWzjDipIkqpaUAj"
        assert cancellation.refund_to == "arc_bsp_cash"
        assert cancellation.refund_currency == "GBP"
        assert cancellation.refund_amount == "90.80"
        assert cancellation.confirmed_at == datetime.datetime(
            2020, 1, 17, 11, 51, 43, 114803
        )
