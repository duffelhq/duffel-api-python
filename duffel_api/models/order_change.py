from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence

from duffel_api.models import Aircraft, Airline, Place
from duffel_api.utils import get_and_transform, parse_datetime


@dataclass
class OrderChangeSlicesSliceSegment:
    """A segment within a slice that is being removed or added"""

    id: str
    aircraft: Optional[Aircraft]
    arriving_at: datetime
    departing_at: datetime
    destination: Place
    destination_terminal: Optional[str]
    origin: Place
    origin_terminal: Optional[str]
    distance: Optional[str]
    duration: Optional[str]
    marketing_carrier: Airline
    marketing_carrier_flight_number: str
    operating_carrier: Airline
    operating_carrier_flight_number: Optional[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            aircraft=get_and_transform(json, "aircraft", Aircraft.from_json),
            arriving_at=datetime.strptime(json["arriving_at"], "%Y-%m-%dT%H:%M:%S"),
            departing_at=datetime.strptime(json["departing_at"], "%Y-%m-%dT%H:%M:%S"),
            destination=Place.from_json(json["destination"]),
            destination_terminal=json.get("destination_terminal"),
            origin=Place.from_json(json["origin"]),
            origin_terminal=json.get("origin_terminal"),
            distance=json.get("distance"),
            duration=json.get("duration"),
            marketing_carrier=Airline.from_json(json["marketing_carrier"]),
            marketing_carrier_flight_number=json["marketing_carrier_flight_number"],
            operating_carrier=Airline.from_json(json["operating_carrier"]),
            operating_carrier_flight_number=json.get("operating_carrier_flight_number"),
        )


@dataclass
class OrderChangeSlicesSlice:
    """A slice that is being removed or added"""

    id: str
    duration: Optional[str]
    destination: Place
    destination_type: str
    origin: Place
    origin_type: str
    segments: Sequence[OrderChangeSlicesSliceSegment]

    allowed_place_types = ["airport", "city"]

    class InvalidPlaceType(Exception):
        """Invalid type of place"""

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            destination_type=json["destination_type"],
            destination=Place.from_json(json["destination"]),
            origin_type=json["origin_type"],
            origin=Place.from_json(json["origin"]),
            duration=json.get("duration"),
            segments=get_and_transform(
                json,
                "segments",
                lambda value: [
                    OrderChangeSlicesSliceSegment.from_json(segment)
                    for segment in value
                ],
                [],
            ),
        )


@dataclass
class OrderChangeSlices:
    """The slices to be added and/or removed"""

    add: Sequence[OrderChangeSlicesSlice]
    remove: Sequence[OrderChangeSlicesSlice]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            add=get_and_transform(
                json,
                "add",
                lambda value: [
                    OrderChangeSlicesSlice.from_json(slice) for slice in value
                ],
                [],
            ),
            remove=get_and_transform(
                json,
                "remove",
                lambda value: [
                    OrderChangeSlicesSlice.from_json(slice) for slice in value
                ],
                [],
            ),
        )


@dataclass
class OrderChange:
    """Once you've created an order change request, and you've chosen which
    slices to add and remove, you'll then want to create an order change.

    To create an order change, you just need to provide the order change offer
    ID.

    If change_total_amount is greater than zero, you will need to provide
    payment details when confirming the change.

    If change_total_amount is less than zero, this amount will be returned to
    the payment method specified by refund_to.
    """

    id: str
    live_mode: bool
    order_id: str
    expires_at: datetime
    change_total_amount: str
    change_total_currency: str
    new_total_amount: str
    new_total_currency: str
    penalty_total_amount: str
    penalty_total_currency: str
    refund_to: str
    slices: OrderChangeSlices
    created_at: datetime
    confirmed_at: Optional[datetime]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            order_id=json["order_id"],
            live_mode=json["live_mode"],
            expires_at=parse_datetime(json["expires_at"]),
            confirmed_at=get_and_transform(json, "confirmed_at", parse_datetime),
            change_total_amount=json["change_total_amount"],
            change_total_currency=json["change_total_currency"],
            new_total_amount=json["new_total_amount"],
            new_total_currency=json["new_total_currency"],
            penalty_total_amount=json["penalty_total_amount"],
            penalty_total_currency=json["penalty_total_currency"],
            refund_to=json["refund_to"],
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            slices=OrderChangeSlices.from_json(json["slices"]),
        )
