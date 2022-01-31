from datetime import date, timedelta

from duffel_api import Duffel

if __name__ == "__main__":
    print("Duffel Flights API - book and change example")
    client = Duffel()
    departure_date = date.today().replace(date.today().year + 1)
    offer_request_slices = [
        {
            "origin": "LHR",
            "destination": "STN",
            "departure_date": departure_date.strftime("%Y-%m-%d"),
        },
    ]
    offer_request = (
        client.offer_requests.create()
        .passengers([{"type": "adult"}])
        .slices(offer_request_slices)
        .execute()
    )

    print(f"Created offer request: {offer_request.id}")

    offers = client.offers.list(offer_request.id)
    offers_list = list(enumerate(offers))

    print(f"Got {len(offers_list)} offers")

    selected_offer = offers_list[0][1]

    print(f"Selected offer {selected_offer.id} to book")

    priced_offer = client.offers.get(selected_offer.id)

    print(
        f"The final price for offer {priced_offer.id} is {priced_offer.total_amount} ({priced_offer.total_currency})"
    )

    payments = [
        {
            "currency": priced_offer.total_currency,
            "amount": priced_offer.total_amount,
            "type": "balance",
        }
    ]
    passengers = [
        {
            "born_on": "1976-01-21",
            "email": "conelia.corde@duffel.com",
            "family_name": "Corde",
            "gender": "f",
            "given_name": "Conelia",
            "id": offer_request.passengers[0].id,
            "phone_number": "+442080160508",
            "title": "ms",
        }
    ]

    order = (
        client.orders.create()
        .payments(payments)
        .passengers(passengers)
        .selected_offers([selected_offer.id])
        .execute()
    )

    print(f"Created order {order.id} with booking reference {order.booking_reference}")

    order_change_request_slices = {
        "add": [
            {
                "cabin_class": "economy",
                "departure_date": (departure_date + timedelta(weeks=4)).strftime(
                    "%Y-%m-%d"
                ),
                "origin": "LHR",
                "destination": "STN",
            }
        ],
        "remove": [
            {
                "slice_id": order.slices[0].id,
            }
        ],
    }

    order_change_request = (
        client.order_change_requests.create(order.id)
        .slices(order_change_request_slices)
        .execute()
    )

    order_change_offers = client.order_change_offers.list(order_change_request.id)
    order_change_offers_list = list(enumerate(order_change_offers))

    print(
        f"Got {len(order_change_offers_list)} options for changing the order; picking first option"
    )

    order_change = client.order_changes.create(order_change_offers_list[0][1].id)

    print(f"Created order change {order_change.id}, confirming...")

    payment = {
        "amount": order_change.change_total_amount,
        "currency": order_change.change_total_currency,
        "type": "balance",
    }

    client.order_changes.confirm(order_change.id, payment)

    print(
        f"Processed change to order {order.id} costing {order_change.change_total_amount} ({order_change.change_total_currency})"
    )
