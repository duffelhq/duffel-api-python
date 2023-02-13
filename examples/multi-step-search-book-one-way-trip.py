from datetime import date, timedelta
from decimal import Decimal

from duffel_api import Duffel


if __name__ == "__main__":
    print(
        "Duffel Flights API - search, book and cancel example for multi-step search - one way"
    )

    client = Duffel()
    departure_date = (date.today() + timedelta(weeks=2)).strftime("%Y-%m-%d")
    slices = [
        {
            "origin": "LHR",
            "destination": "STN",
            "departure_date": departure_date,
        },
    ]

    partial_offer_request = (
        client.partial_offer_requests.create()
        .passengers([{"type": "adult"}])
        .slices(slices)
        .execute()
    )

    print(f"Created partial offer request: {partial_offer_request.id}")

    offers_list = list(enumerate(partial_offer_request.offers))
    print(f"Got {len(offers_list)} outbound offers")
    outbound_partial_offer_id = offers_list[0][1].id
    print(f"Selected offer {outbound_partial_offer_id} to search for inbound")

    fares_offer_request = client.partial_offer_requests.fares(
        partial_offer_request.id, [outbound_partial_offer_id]
    )
    offers_list = list(enumerate(fares_offer_request.offers))
    print(f"Got {len(offers_list)} full offers")
    selected_offer = offers_list[0][1]

    priced_offer = client.offers.get(selected_offer.id, return_available_services=True)

    print(
        f"The final price for offer {priced_offer.id} is {priced_offer.total_amount} ({priced_offer.total_currency})"
    )

    available_service = priced_offer.available_services[0]

    print(
        f"Adding an extra bag with service {available_service.id}, costing {available_service.total_amount} ({available_service.total_currency})"
    )

    total_amount = str(
        Decimal(priced_offer.total_amount) + Decimal(available_service.total_amount)
    )
    payments = [
        {
            "currency": selected_offer.total_currency,
            "amount": total_amount,
            "type": "balance",
        }
    ]
    services = [
        {
            "id": available_service.id,
            "quantity": 1,
        }
    ]
    passengers = [
        {
            "born_on": "1976-01-21",
            "email": "conelia.corde@duffel.com",
            "family_name": "Corde",
            "gender": "f",
            "given_name": "Conelia",
            "id": partial_offer_request.passengers[0].id,
            "phone_number": "+442080160508",
            "title": "ms",
        }
    ]

    print(total_amount)
    print(payments)
    print(services)
    print(passengers)
    order = (
        client.orders.create()
        .payments(payments)
        .passengers(passengers)
        .selected_offers([selected_offer.id])
        .services(services)
        .execute()
    )

    print(f"Created order {order.id} with booking reference {order.booking_reference}")

    order_cancellation = client.order_cancellations.create(order.id)

    print(
        f"Requested refund quote for order {order.id} – {order_cancellation.refund_amount} ({order_cancellation.refund_currency}) is available"
    )

    client.order_cancellations.confirm(order_cancellation.id)

    print(f"Confirmed refund quote for order {order.id}")
