import pytest

from duffel_api.api import OrderCreate, OrderUpdate

from .fixtures import fixture


def test_get_order_by_id(requests_mock):
    url = "air/orders/id"
    with fixture("get-order-by-id", url, requests_mock.get, 200) as client:
        order = client.orders.get("id")
        assert order.id == "ord_00009hthhsUZ8W4LxQgkjo"
        assert len(order.slices) == 1
        assert len(order.passengers) == 1
        assert not order.live_mode
        slice = order.slices[0]
        assert slice.origin_type == "airport"


def test_get_orders(requests_mock):
    # We need a way to ensure pagination finished in a mocking environment
    end_pagination_url = (
        "http://someaddress/air/orders?limit=50"
        + "&after=g2wAAAACbQAAABBBZXJvbWlzdC1LaGFya2l2bQAAAB%3D"
    )
    end_pagination_response = {"meta": {"after": None}, "data": []}
    requests_mock.get(
        end_pagination_url, complete_qs=True, json=end_pagination_response
    )

    url = "air/orders?limit=50"
    with fixture("get-orders", url, requests_mock.get, 200) as client:
        paginated_orders = client.orders.list()
        orders = list(paginated_orders)
        assert len(orders) == 1
        order = orders[0]
        assert order.id == "ord_00009hthhsUZ8W4LxQgkjo"


def test_create_order(requests_mock):
    url = "air/orders"
    with fixture("create-order", url, requests_mock.post, 201) as client:
        passengers = [
            {
                "born_on": "2000-02-21",
                "email": "3124@example.com",
                "family_name": "Doe",
                "given_name": "Jane",
                "gender": "f",
                "id": "pas_00009hj8USM7Ncg31cBCLL",
                "phone_number": "00333333333",
                "title": "miss",
            }
        ]
        payments = [{"amount": "32", "currency": "GBP", "type": "balance"}]
        creation = client.orders.create()
        order = (
            creation.passengers(passengers)
            .selected_offers(["offer-id"])
            .payments(payments)
            .execute()
        )
        assert order.id == "ord_00009hthhsUZ8W4LxQgkjo"
        assert len(order.services) == 1
        service = order.services[0]
        assert service.id == "ser_00009UhD4ongolulWd9123"


def test_create_order_with_invalid_data(requests_mock):
    url = "air/orders"
    with fixture("create-order", url, requests_mock.post, 422) as client:
        creation = client.orders.create()
        with pytest.raises(OrderCreate.InvalidNumberOfPassengers):
            creation.execute()

        with pytest.raises(OrderCreate.InvalidPassenger):
            creation.passengers([{}]).execute()

        passengers = [
            {
                "born_on": "2000-02-21",
                "email": "3124@example.com",
                "family_name": "Doe",
                "given_name": "Jane",
                "gender": "f",
                "id": "pas_00009hj8USM7Ncg31cBCLL",
                "phone_number": "00333333333",
                "title": "miss",
            }
        ]

        selected_offers = ["offer-id"]
        payments = [{"amount": "32", "currency": "GBP", "type": "balance"}]

        # from this point we have valid passengers
        creation = creation.passengers(passengers)
        with pytest.raises(OrderCreate.InvalidNumberOfPayments):
            creation.execute()

        with pytest.raises(OrderCreate.InvalidPayment):
            creation.payments([{}]).execute()

        # from this point we have valid payments
        creation = creation.payments(payments)
        with pytest.raises(OrderCreate.InvalidSelectedOffersLength):
            creation.execute()

        with pytest.raises(OrderCreate.InvalidService):
            creation.selected_offers(selected_offers).services([{}]).execute()


def test_update_order(requests_mock):
    url = "air/orders/ord_00009hthhsUZ8W4LxQgkjo"
    with fixture("update-order-by-id", url, requests_mock.patch, 200) as client:
        order = (
            client.orders.update("ord_00009hthhsUZ8W4LxQgkjo")
            .metadata(
                {
                    "customer_prefs": "window seat",
                    "payment_intent_id": "pit_00009htYpSCXrwaB9DnUm2",
                }
            )
            .execute()
        )

        assert order.id == "ord_00009hthhsUZ8W4LxQgkjo"
        assert order.metadata == {
            "customer_prefs": "window seat",
            "payment_intent_id": "pit_00009htYpSCXrwaB9DnUm2",
        }


def test_update_order_with_invalid_data(requests_mock):
    url = "air/orders/ord_00009hthhsUZ8W4LxQgkjo"
    with fixture("update-order-by-id", url, requests_mock.patch, 422) as client:
        updating = client.orders.update("ord_00009hthhsUZ8W4LxQgkjo")

        with pytest.raises(OrderUpdate.InvalidMetadata):
            updating.metadata(1).execute()
