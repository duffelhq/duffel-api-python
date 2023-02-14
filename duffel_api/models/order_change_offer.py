from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence

from duffel_api.models import Aircraft, Airline, Place, Airport
from duffel_api.utils import get_and_transform, parse_datetime


@dataclass
class OrderChangeOfferSlicesSliceSegment:
    """A segment within a slice that is being removed or added"""

    id: str
    aircraft: Optional[Aircraft]
    arriving_at: datetime
    departing_at: datetime
    destination: Airport
    destination_terminal: Optional[str]
    origin: Airport
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
            destination=Airport.from_json(json["destination"]),
            destination_terminal=json.get("destination_terminal"),
            origin=Airport.from_json(json["origin"]),
            origin_terminal=json.get("origin_terminal"),
            distance=json.get("distance"),
            duration=json.get("duration"),
            marketing_carrier=Airline.from_json(json["marketing_carrier"]),
            marketing_carrier_flight_number=json["marketing_carrier_flight_number"],
            operating_carrier=Airline.from_json(json["operating_carrier"]),
            operating_carrier_flight_number=json.get("operating_carrier_flight_number"),
        )


@dataclass
class OrderChangeOfferSlicesSlice:
    """A slice that is being removed or added"""

    id: str
    duration: Optional[str]
    destination: Place
    destination_type: str
    origin: Place
    origin_type: str
    segments: Sequence[OrderChangeOfferSlicesSliceSegment]

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
                    OrderChangeOfferSlicesSliceSegment.from_json(segment)
                    for segment in value
                ],
                [],
            ),
        )


@dataclass
class OrderChangeOfferSlices:
    """The slices to be added and/or removed"""

    add: Sequence[OrderChangeOfferSlicesSlice]
    remove: Sequence[OrderChangeOfferSlicesSlice]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            add=get_and_transform(
                json,
                "add",
                lambda value: [
                    OrderChangeOfferSlicesSlice.from_json(slice) for slice in value
                ],
                [],
            ),
            remove=get_and_transform(
                json,
                "remove",
                lambda value: [
                    OrderChangeOfferSlicesSlice.from_json(slice) for slice in value
                ],
                [],
            ),
        )


@dataclass
class OrderChangeOffer:
    """After you've searched for flights to add to your order by creating an order change
    request, we'll send your search to a range of airlines, which may return order change
    offers.

    Each order change offer represents flights you can buy from an airline at a particular
    price that meets your search criteria.

    You'll see slices inside the offers. Each slice will also include a list of one or
    more specific flights (called segments) that the airline is offering to get the
    passengers where they want to go.
    """

    id: str
    order_change_id: str
    live_mode: bool
    change_total_amount: str
    change_total_currency: Optional[str]
    new_total_amount: Optional[str]
    new_total_currency: str
    penalty_amount: Optional[str]
    penalty_currency: Optional[str]
    refund_to: str
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    slices: OrderChangeOfferSlices

    allowed_refund_types = [
        "arc_bsp_cash",
        "balance",
        "card",
        "original_form_of_payment",
        "voucher",
        "awaiting_payment",
    ]

    class InvalidRefundType(Exception):
        """Invalid refund type provided"""

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            order_change_id=json["order_change_id"],
            live_mode=json["live_mode"],
            change_total_amount=json["change_total_amount"],
            change_total_currency=json.get("change_total_currency"),
            new_total_amount=json.get("new_total_amount"),
            new_total_currency=json["new_total_currency"],
            penalty_amount=json.get("penalty_amount"),
            penalty_currency=json.get("penalty_currency"),
            refund_to=json["refund_to"],
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            updated_at=datetime.strptime(json["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            expires_at=parse_datetime(json["expires_at"]),
            slices=OrderChangeOfferSlices.from_json(json["slices"]),
        )
