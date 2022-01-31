from datetime import date

from duffel_api import Duffel


if __name__ == "__main__":
    print("Duffel Flights API - book with adult and infant example")
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
        .passengers(
            [{"type": "adult"}, {"age": 1}, {"age": (date.today().year - 2003)}]
        )
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

    print(
        "The final price for offer %s is %s (%s)"
        % (priced_offer.id, priced_offer.total_amount, priced_offer.total_currency)
    )

    payments = [
        {
            "currency": selected_offer.total_currency,
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
            "infant_passenger_id": offer_request.passengers[1].id,
            "phone_number": "+442080160508",
            "title": "ms",
        },
        {
            "born_on": date.today().replace(date.today().year - 1).strftime("%Y-%m-%d"),
            "email": "baby.corde@duffel.com",
            "family_name": "Corde",
            "gender": "f",
            "given_name": "Baby",
            "id": offer_request.passengers[1].id,
            "phone_number": "+442080160508",
            "title": "miss",
        },
        {
            "born_on": "2003-10-24",
            "email": "constantine.corde@duffel.com",
            "family_name": "Corde",
            "gender": "m",
            "given_name": "Constantine",
            "id": offer_request.passengers[2].id,
            "phone_number": "+442080160508",
            "title": "mr",
        },
    ]

    order = (
        client.orders.create()
        .payments(payments)
        .passengers(passengers)
        .selected_offers([selected_offer.id])
        .execute()
    )

    print(
        "Created order %s with booking reference %s"
        % (order.id, order.booking_reference)
    )

    order_cancellation = client.order_cancellations.create(order.id)

    print(
        "Requested refund quote for order %s – %s (%s) is available"
        % (
            order.id,
            order_cancellation.refund_amount,
            order_cancellation.refund_currency,
        )
    )

    client.order_cancellations.confirm(order_cancellation.id)

    print("Confirmed refund quote for order %s" % (order.id))
