from datetime import date

from duffel_api import Duffel


if __name__ == "__main__":
    print("Duffel Flights API - book hold order and pay later example")
    client = Duffel()
    departure_date = date.today().replace(date.today().year + 1)
    slices = [
        {
            "origin": "LHR",
            "destination": "STN",
            "departure_date": departure_date.strftime("%Y-%m-%d"),
        },
    ]
    offer_request = (
        client.offer_requests.create()
        .passengers([{"type": "adult"}])
        .slices(slices)
        .execute()
    )

    print(f"Created offer request: {offer_request.id}")

    offers = client.offers.list(offer_request.id)
    offers_list = list(enumerate(offers))

    print(f"Got {len(offers_list)} offers")

    selected_offer = offers_list[0][1]

    print(f"Selected offer {selected_offer.id} to book")

    priced_offer = client.offers.get(selected_offer.id)
    passengers = [
        {
            "born_on": "1976-01-21",
            "email": "conelia.corde@example.com",
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
        .passengers(passengers)
        .selected_offers([selected_offer.id])
        .hold()
        .execute()
    )

    print(
        f"Created hold order {order.id} with booking reference {order.booking_reference}"
    )

    updated_order = client.orders.get(order.id)

    print(
        f"Retrieved order and up-to-date price is {updated_order.total_amount} ({updated_order.total_currency})"
    )

    payment = (
        client.payments.create()
        .order(order.id)
        .payment(
            {
                "currency": updated_order.total_currency,
                "amount": updated_order.total_amount,
                "type": "balance",
            }
        )
        .execute()
    )

    print(f"Paid for order {order.id} with payment {payment.id}")

    paid_order = client.orders.get(order.id)

    print(f"After payment, order has {len(paid_order.documents)} documents")
