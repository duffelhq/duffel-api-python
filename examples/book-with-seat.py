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
        f"Adding seat {available_seat.designator} costing {available_seat_service.total_amount} ({available_seat_service.total_currency})"
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
        .payments(payments)
        .passengers(passengers)
        .selected_offers([selected_offer.id])
        .services(services)
        .execute()
    )

    print(f"Created order {order.id} with booking reference {order.booking_reference}")
