from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, Union

from duffel_api.models import Aircraft, Airline, Airport, LoyaltyProgrammeAccount, Place
from duffel_api.utils import get_and_transform


@dataclass
class OrderConditionChangeBeforeDeparture:
    """Whether the whole order can be changed before the departure of the first slice.

    If all of the slices on the order can be changed then
    the `allowed` property will be `true`. Refer to the `slices` for
    information about change penalties.

    If any of the slices on the order can't be changed then
    the `allowed` property will be `false`. In this case you should
    refer to the `slices` conditions to determine if any part
    of the order is changeable.

    If the airline hasn't provided any information about whether
    this order can be changed then this property will be `null`.
    """

    allowed: bool
    penalty_amount: Optional[str]
    penalty_currency: Optional[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            allowed=json["allowed"],
            penalty_amount=json.get("penalty_amount"),
            penalty_currency=json.get("penalty_currency"),
        )


@dataclass
class OrderConditionRefundBeforeDeparture:
    """Whether the whole order can be refunded before the departure of the first slice.

    If all of the slices on the order can be refunded then
    the `allowed` property will be `true` and information will be
    provided about any penalties.

    If any of the slices on the order can't be refunded then
    the `allowed` property will be `false`.

    If the airline hasn't provided any information about whether
    this order can be refunded then this property will be `null`.
    """

    allowed: bool
    penalty_amount: Optional[str]
    penalty_currency: Optional[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            allowed=json["allowed"],
            penalty_amount=json.get("penalty_amount"),
            penalty_currency=json.get("penalty_currency"),
        )


@dataclass
class OrderConditions:
    """The conditions associated with this order, describing the kinds of
    modifications you can make to it and any penalties that
    will apply to those modifications.

    This information assumes the condition is applied to all of the slices and passengers
    associated with this order - for information at the slice level
    (e.g. "what happens if I just want to change the first slice?") refer to the `slices`.

    If a particular kind of modification is allowed, you may not always be able to take
    action through the Duffel API. In some cases, you may need to contact the Duffel
    support team or the airline directly.
    """

    change_before_departure: Optional[OrderConditionChangeBeforeDeparture]
    refund_before_departure: Optional[OrderConditionRefundBeforeDeparture]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            change_before_departure=get_and_transform(
                json,
                "change_before_departure",
                OrderConditionChangeBeforeDeparture.from_json,
            ),
            refund_before_departure=get_and_transform(
                json,
                "refund_before_departure",
                OrderConditionRefundBeforeDeparture.from_json,
            ),
        )


@dataclass
class OrderSliceSegmentPassengerSeat:
    """An object containing metadata about the service, like the designator of the seat"""

    designator: str
    name: str
    disclosures: Sequence[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            designator=json["designator"],
            name=json["name"],
            disclosures=json["disclosures"],
        )


@dataclass
class OrderSliceSegmentPassengerBaggage:
    """The baggage allowances for the passenger on this segment that were included in the
    original offer. Any extra baggage items which were booked as services will be listed
    in the services field instead of here.
    """

    type: str
    quantity: int

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            type=json["type"],
            quantity=json["quantity"],
        )


@dataclass
class OrderSliceSegmentPassenger:
    """Additional segment-specific information about the passengers included in the offer
    (e.g. their baggage allowance and the cabin class they will be travelling in)
    """

    baggages: Sequence[OrderSliceSegmentPassengerBaggage]
    cabin_class: str
    cabin_class_marketing_name: str
    passenger_id: str
    seat: Optional[OrderSliceSegmentPassengerSeat]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            baggages=get_and_transform(
                json,
                "baggages",
                lambda value: [
                    OrderSliceSegmentPassengerBaggage.from_json(baggage)
                    for baggage in value
                ],
                [],
            ),
            cabin_class=json["cabin_class"],
            cabin_class_marketing_name=json["cabin_class_marketing_name"],
            passenger_id=json["passenger_id"],
            seat=get_and_transform(
                json, "seat", OrderSliceSegmentPassengerSeat.from_json
            ),
        )


@dataclass
class OrderSliceSegment:
    """The segments - that is, specific flights - that the airline is offering to get the
    passengers from the `origin` to the `destination`
    """

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
    passengers: Sequence[OrderSliceSegmentPassenger]

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
            passengers=get_and_transform(
                json,
                "passengers",
                lambda value: [
                    OrderSliceSegmentPassenger.from_json(passenger)
                    for passenger in value
                ],
                [],
            ),
        )


@dataclass
class OrderSliceConditionChangeBeforeDeparture:
    """Whether this slice can be changed before the departure.

    If the slice can be changed for all of the passengers then
    the `allowed` property will be `true` and information will be
    provided about any penalties.

    If none of the passengers on the slice can be changed then
    the `allowed` property will be `false`.

    In all other cases this property will be `null` indicating we
    can't provide the information for this slice.

    The `penalty_amount` is specific to changing this slice and may not be
    the penalties that is applied if the entire order is changed.
    """

    allowed: bool
    penalty_amount: Optional[str]
    penalty_currency: Optional[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            allowed=json["allowed"],
            penalty_amount=json.get("penalty_amount"),
            penalty_currency=json.get("penalty_currency"),
        )


@dataclass
class OrderSliceConditions:
    """The conditions associated with this slice, describing the kinds of
    modifications you can make and any penalties that
    will apply to those modifications.

    This condition is applied only to this slice and to all the passengers
    associated with this order - for information at the order level
    (e.g. "what happens if I want to change all the slices?") refer to the
    `conditions` at the top level.

    If a particular kind of modification is allowed, you may not always be able to take
    action through the Duffel API. In some cases, you may need to contact the Duffel
    support team or
    the airline directly.
    """

    change_before_departure: Optional[OrderSliceConditionChangeBeforeDeparture]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            change_before_departure=get_and_transform(
                json,
                "change_before_departure",
                OrderSliceConditionChangeBeforeDeparture.from_json,
            )
        )


@dataclass
class OrderSlice:
    """A slice is one part of the slices that make up the itinerary of an order.
    One-way journeys can be expressed using one slice, whereas return trips will need two.
    """

    id: str
    changeable: bool
    destination_type: str
    destination: Place
    origin_type: str
    origin: Place
    duration: Optional[str]
    segments: Sequence[OrderSliceSegment]
    conditions: OrderSliceConditions

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            changeable=json["changeable"],
            destination_type=json["destination_type"],
            destination=Place.from_json(json["destination"]),
            origin_type=json["origin_type"],
            origin=Place.from_json(json["origin"]),
            duration=json.get("duration"),
            segments=get_and_transform(
                json,
                "segments",
                lambda value: [
                    OrderSliceSegment.from_json(segment) for segment in value
                ],
                [],
            ),
            conditions=OrderSliceConditions.from_json(json["conditions"]),
        )


@dataclass
class OrderServiceMetadataSeat:
    """An object containing metadata about the service, like the designator of the seat"""

    designator: str
    name: str
    disclosures: Sequence[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            designator=json["designator"],
            name=json["name"],
            disclosures=json["disclosures"],
        )


@dataclass
class OrderServiceMetadataBaggage:
    """An object containing metadata about the service, like the maximum weight and
    dimensions of the baggage.
    """

    type: str
    maximum_weight_kg: Optional[int]
    maximum_height_cm: Optional[int]
    maximum_length_cm: Optional[int]
    maximum_depth_cm: Optional[int]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            type=json["type"],
            maximum_weight_kg=json.get("maximum_weight_kg"),
            maximum_height_cm=json.get("maximum_height_cm"),
            maximum_length_cm=json.get("maximum_length_cm"),
            maximum_depth_cm=json.get("maximum_depth_cm"),
        )


@dataclass
class OrderService:
    """The service booked along with this order"""

    id: str
    metadata: Union[OrderServiceMetadataSeat, OrderServiceMetadataBaggage]
    passenger_ids: Sequence[str]
    quantity: int
    segment_ids: Sequence[str]
    total_amount: str
    total_currency: str
    type: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        type = json["type"]
        metadata = json["metadata"]

        if type == "seat":
            metadata = OrderServiceMetadataSeat.from_json(metadata)
        elif type == "baggage":
            metadata = OrderServiceMetadataBaggage.from_json(metadata)

        return cls(
            id=json["id"],
            metadata=metadata,
            passenger_ids=json["passenger_ids"],
            quantity=json["quantity"],
            segment_ids=json["segment_ids"],
            total_amount=json["total_amount"],
            total_currency=json["total_currency"],
            type=type,
        )


@dataclass
class OrderPaymentStatus:
    """The payment status for an order"""

    awaiting_payment: bool
    payment_required_by: Optional[datetime]
    price_guarantee_expires_at: Optional[datetime]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            awaiting_payment=json["awaiting_payment"],
            payment_required_by=get_and_transform(
                json,
                "payment_required_by",
                lambda value: datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ"),
            ),
            price_guarantee_expires_at=get_and_transform(
                json,
                "price_guarantee_expires_at",
                lambda value: datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ"),
            ),
        )


@dataclass
class OrderPassenger:
    """A passenger who is travelling"""

    id: str
    type: str
    infant_passenger_id: Optional[str]
    given_name: str
    family_name: str
    gender: str
    title: str
    born_on: str
    loyalty_programme_accounts: Sequence[LoyaltyProgrammeAccount]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            type=json["type"],
            infant_passenger_id=json.get("infant_passenger_id"),
            given_name=json["given_name"],
            family_name=json["family_name"],
            gender=json["gender"],
            title=json["title"],
            born_on=json["born_on"],
            loyalty_programme_accounts=get_and_transform(
                json,
                "loyalty_programme_accounts",
                lambda value: [
                    LoyaltyProgrammeAccount.from_json(loyalty_programme_account)
                    for loyalty_programme_account in value
                ],
                [],
            ),
        )


@dataclass
class OrderDocument:
    """A document issued for this order."""

    type: str
    unique_identifier: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            type=json["type"],
            unique_identifier=json["unique_identifier"],
        )


@dataclass
class Order:
    """Once you've searched for flights by creating an offer request, and you've chosen
    which offer you want to book, you'll then want to create an order.

    To create an order, you just need to provide the offer ID, payment details and some
    additional information on the passengers (e.g. their full name and date of birth).
    """

    id: str
    live_mode: bool
    available_actions: Sequence[str]
    base_amount: Optional[str]
    base_currency: Optional[str]
    booking_reference: str
    cancelled_at: Optional[datetime]
    content: str
    created_at: datetime
    synced_at: Optional[datetime]
    documents: Sequence[OrderDocument]
    passengers: Sequence[OrderPassenger]
    payment_status: OrderPaymentStatus
    services: Sequence[OrderService]
    slices: Sequence[OrderSlice]
    conditions: OrderConditions
    owner: Airline
    tax_amount: str
    tax_currency: Optional[str]
    total_amount: str
    total_currency: str
    metadata: dict

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            available_actions=json["available_actions"],
            live_mode=json["live_mode"],
            base_amount=json.get("base_amount"),
            base_currency=json.get("base_currency"),
            booking_reference=json["booking_reference"],
            cancelled_at=get_and_transform(
                json,
                "cancelled_at",
                lambda value: datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ"),
            ),
            content=json["content"],
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            synced_at=get_and_transform(
                json,
                "synced_at",
                lambda value: datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ"),
            ),
            documents=get_and_transform(
                json,
                "documents",
                lambda value: [OrderDocument.from_json(document) for document in value],
                [],
            ),
            owner=Airline.from_json(json["owner"]),
            passengers=get_and_transform(
                json,
                "passengers",
                lambda value: [
                    OrderPassenger.from_json(passenger) for passenger in value
                ],
                [],
            ),
            payment_status=OrderPaymentStatus.from_json(json["payment_status"]),
            services=get_and_transform(
                json,
                "services",
                lambda value: [OrderService.from_json(service) for service in value],
                [],
            ),
            slices=get_and_transform(
                json,
                "slices",
                lambda value: [OrderSlice.from_json(slice) for slice in value],
                [],
            ),
            conditions=OrderConditions.from_json(json["conditions"]),
            tax_amount=json["tax_amount"],
            tax_currency=json.get("tax_currency"),
            total_amount=json["total_amount"],
            total_currency=json["total_currency"],
            # Metadata is customer-specified data, so we don't try and parse it
            metadata=json["metadata"],
        )
