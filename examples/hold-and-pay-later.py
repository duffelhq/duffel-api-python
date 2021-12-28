from datetime import date, timedelta

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

    print("Created offer request: %s" % (offer_request.id))

    offers = client.offers.list(offer_request.id)
    offers_list = list(enumerate(offers))

    print("Got %d offers" % len(offers_list))

    selected_offer = offers_list[0][1]

    print("Selected offer %s to book" % (selected_offer.id))

    priced_offer = client.offers.get(selected_offer.id)
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
        .passengers(passengers)
        .selected_offers([selected_offer.id])
        .hold()
        .execute()
    )

    print(
        "Created hold order %s with booking reference %s"
        % (order.id, order.booking_reference)
    )

    updated_order = client.orders.get(order.id)

    print(
        "Retrieved order and up-to-date price is %s (%s)"
        % (updated_order.total_amount, updated_order.total_currency)
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

    print("Paid for order %s with payment %s" % (order.id, payment.id))

    paid_order = client.orders.get(order.id)

    print("After payment, order has %d documents" % len(paid_order.documents))
