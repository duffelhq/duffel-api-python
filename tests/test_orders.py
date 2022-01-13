from datetime import datetime

import pytest

from duffel_api.api import OrderCreate, OrderUpdate

from .fixtures import fixture


def test_get_order_by_id(requests_mock):
    url = "air/orders/id"
    with fixture("get-order-by-id", url, requests_mock.get, 200) as client:
        order = client.orders.get("id")
        assert order.id == "ord_00009hthhsUZ8W4LxQgkjo"
        assert not order.live_mode
        assert order.payment_status.awaiting_payment
        assert len(order.passengers) == 1
        assert order.synced_at == datetime(2020, 4, 11, 15, 48, 11)
        assert len(order.slices) == 1
        slice = order.slices[0]
        assert slice.conditions.change_before_departure.allowed
        assert slice.origin_type == "airport"
        assert len(order.slices[0].segments) == 1
        assert len(order.slices[0].segments[0].passengers) == 1
        passenger = order.slices[0].segments[0].passengers[0]
        assert len(passenger.baggages) == 1
        assert passenger.baggages[0].quantity == 1
        assert passenger.baggages[0].type == "checked"
        assert passenger.cabin_class == "economy"
        assert passenger.cabin_class_marketing_name == "Economy Basic"
        assert passenger.passenger_id == "passenger_0"
        assert passenger.seat is not None
        assert passenger.seat.designator == "14B"
        assert len(passenger.seat.disclosures) == 2
        assert passenger.seat.disclosures[0] == "Do not seat children in exit row seats"
        assert (
            passenger.seat.disclosures[1]
            == "Do not seat passengers with special needs in exit row seats"
        )
        assert passenger.seat.name == "Exit row seat"


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
        assert len(order.slices) == 1
        assert len(order.slices[0].segments) == 1
        assert len(order.slices[0].segments[0].passengers) == 1
        passenger = order.slices[0].segments[0].passengers[0]
        assert len(passenger.baggages) == 1
        assert passenger.baggages[0].quantity == 1
        assert passenger.baggages[0].type == "checked"
        assert passenger.cabin_class == "economy"
        assert passenger.cabin_class_marketing_name == "Economy Basic"
        assert passenger.passenger_id == "passenger_0"
        assert passenger.seat is None
        assert order.synced_at == datetime(2020, 4, 11, 15, 48, 11)


def test_create_instant_order(requests_mock):
    url = "air/orders"
    with fixture("create-instant-order", url, requests_mock.post, 201) as client:
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
        assert order.payment_status.awaiting_payment is False
        assert order.payment_status.payment_required_by is None
        assert order.payment_status.price_guarantee_expires_at is None
        assert order.synced_at == datetime(2020, 4, 11, 15, 48, 11)
        assert len(order.services) == 1
        service = order.services[0]
        assert service.id == "ser_00009UhD4ongolulWd9123"


def test_create_hold_order(requests_mock):
    url = "air/orders"
    with fixture("create-hold-order", url, requests_mock.post, 201) as client:
        passengers = [
            {
                "born_on": "2000-01-12",
                "email": "8567@example.com",
                "family_name": "Doe",
                "given_name": "Jack",
                "gender": "m",
                "id": "pas_00009hj8USM7Ncg31cBANZ",
                "phone_number": "00333333333",
                "title": "mr",
            }
        ]
        creation = client.orders.create()
        order = (
            creation.passengers(passengers)
            .selected_offers(["offer-id"])
            .hold()
            .execute()
        )
        assert order.id == "ord_00009hthhsUZ8W4LxQgkjo"
        assert order.payment_status.awaiting_payment is True
        assert order.payment_status.payment_required_by == datetime(
            2020, 1, 17, 10, 42, 14
        )
        assert order.payment_status.price_guarantee_expires_at == datetime(
            2020, 1, 17, 10, 42, 14
        )
        assert order.synced_at == datetime(2020, 4, 11, 15, 48, 11)
        assert len(order.services) == 1
        service = order.services[0]
        assert service.id == "ser_00009UhD4ongolulWd9123"


def test_create_order_with_invalid_data(requests_mock):
    url = "air/orders"
    with fixture("create-instant-order", url, requests_mock.post, 422) as client:
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
        assert order.synced_at == datetime(2020, 4, 11, 15, 48, 11)
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
