from datetime import date
import os

from duffel_api import Duffel
from duffel_api.http_client import ApiError


if __name__ == "__main__":
    print("Duffel Flights API - Python Example on handling errors")

    os.environ["DUFFEL_ACCESS_TOKEN"] = "some-invalid-token-to-trigger-an-error"

    client = Duffel()
    departure_date = date.today().replace(date.today().year + 1)
    slices = [
        {
            "origin": "LHR",
            "destination": "STN",
            "departure_date": departure_date.strftime("%Y-%m-%d"),
        },
    ]
    try:
        offer_request = (
            client.offer_requests.create()
            .passengers(
                [{"type": "adult"}, {"age": 1}, {"age": (date.today().year - 2003)}]
            )
            .slices(slices)
            .execute()
        )
    except ApiError as exc:
        # This is super useful when contacting Duffel support
        print(f"Request ID: {exc.meta['request_id']}")
        print(f"Status Code: {exc.meta['status']}")
        print("Errors: ")
        for error in exc.errors:
            print(f" Title: {error['title']}")
            print(f" Code: {error['code']}")
            print(f" Message: {error['message']}")
