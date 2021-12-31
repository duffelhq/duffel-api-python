from datetime import date
from decimal import Decimal

from duffel_api import Duffel


if __name__ == "__main__":
    print("Duffel Flights API - book with seat example")
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

    print(
        "The final price for offer %s is %s (%s)"
        % (priced_offer.id, priced_offer.total_amount, priced_offer.total_currency)
    )

    seat_maps = client.seat_maps.get(priced_offer.id)

    available_seats = []
    for _idx, row in enumerate(seat_maps[0].cabins[0].rows):
        for _idx, section in enumerate(row.sections):
            for _idx, element in enumerate(section.elements):
                if (
                    element.type == "seat"
                    and element.available_services is not None
                    and len(element.available_services) > 0
                ):
                    available_seats.append(element)

    available_seat = available_seats[0]

    available_seat_service = available_seat.available_services[0]

    print(
        "Adding seat %s costing %s (%s)"
        % (
            available_seat.designator,
            available_seat_service.total_amount,
            available_seat_service.total_currency,
        )
    )

    total_amount = str(
        Decimal(priced_offer.total_amount)
        + Decimal(available_seat_service.total_amount)
    )

    services = [
        {
            "id": available_seat_service.id,
            "quantity": 1,
        }
    ]
    payments = [
        {
            "currency": priced_offer.total_currency,
            "amount": total_amount,
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
        .services(services)
        .execute()
    )

    print(
        "Created order %s with booking reference %s"
        % (order.id, order.booking_reference)
    )
