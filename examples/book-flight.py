from duffel_api import Duffel


if __name__ == "__main__":
    print("Duffel Flights API - Python Example")
    client = Duffel()

    destination = input("\nWhere do you want to go?\n").strip()
    origin = input("\nFrom where?\n").strip()
    departure_date = input("\nOn what date? (YYYY-MM-DD)\n").strip()

    print("\nSearching flights...")

    slices = [
        {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
        },
    ]
    offer_request = (
        client.offer_requests.create()
        .passengers([{"type": "adult"}])
        .slices(slices)
        .return_offers()
        .execute()
    )
    offers = offer_request.offers

    for idx, offer in enumerate(offers):
        print(
            f"{idx + 1}. {offer.owner.name} flight departing at "
            + f"{offer.slices[0].segments[0].departing_at} "
            + f"{offer.total_amount} {offer.total_currency}"
        )

    offer_index = input("\nWhich offer do you wish to book?\n").strip()

    given_name = input("\nWhat's your given name?\n").strip()
    family_name = input("\nWhat's your family name?\n").strip()
    dob = input("\nWhat's your date of birth? (YYYY-MM-DD)\n").strip()
    title = input("\nWhat's your title? (mr, ms, mrs, miss)\n").strip()
    gender = input("\nWhat's your gender? (m, f)\n").strip()
    phone_number = input("\nWhat's your phone number? (+XX)\n").strip()
    email = input("\nWhat's your email address?\n").strip()
    print(f"\nHang tight! Booking offer {offer_index}...")

    selected_offer = offers[int(offer_index) - 1]
    payments = [
        {
            "currency": selected_offer.total_currency,
            "amount": selected_offer.total_amount,
            "type": "balance",
        }
    ]
    passengers = [
        {
            "phone_number": phone_number,
            "email": email,
            "title": title,
            "gender": gender,
            "family_name": family_name,
            "given_name": given_name,
            "born_on": dob,
            "id": offer_request.passengers[0].id,
        }
    ]

    order = (
        client.orders.create()
        .payments(payments)
        .passengers(passengers)
        .selected_offers([selected_offer.id])
        .execute()
    )

    print("\n🎉 Flight booked. Congrats! You can start packing your (duffel?) bags")
    print(f"Booking reference: {order.booking_reference}")
