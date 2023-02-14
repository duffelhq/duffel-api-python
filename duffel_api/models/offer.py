from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence

from duffel_api.models import Aircraft, Airline, Airport, LoyaltyProgrammeAccount, Place
from duffel_api.utils import get_and_transform, parse_datetime


@dataclass
class OfferConditionChangeBeforeDeparture:
    """Whether the whole offer can be changed before the departure of the first slice.

    If all of the slices on the offer can be changed then the allowed property will be
    true. Refer to the slices for information about change penalties. If any of the slices
    on the offer can't be changed then the allowed property will be false. In this case
    you should refer to the slices conditions to determine if any part of the offer is
    changeable. If the airline hasn't provided any information about whether this offer
    can be changed then this property will be null.
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
class OfferConditionRefundBeforeDeparture:
    """Whether the whole offer can be refunded before the departure of the first slice.

    If all of the slices on the offer can be refunded then the allowed property will be
    true and information will be provided about any penalties. If any of the slices on the
    offer can't be refunded then the allowed property will be false. If the airline hasn't
    provided any information about whether this offer can be refunded then this property
    will be null.
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
class OfferConditions:
    """The conditions associated with this offer, describing the kinds of modifications
    you can make post-booking and any penalties that will apply to those modifications.
    """

    change_before_departure: Optional[OfferConditionChangeBeforeDeparture]
    refund_before_departure: Optional[OfferConditionRefundBeforeDeparture]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            change_before_departure=get_and_transform(
                json,
                "change_before_departure",
                OfferConditionChangeBeforeDeparture.from_json,
            ),
            refund_before_departure=get_and_transform(
                json,
                "refund_before_departure",
                OfferConditionRefundBeforeDeparture.from_json,
            ),
        )


@dataclass
class PaymentRequirements:
    """The payment requirements for an offer"""

    payment_required_by: Optional[datetime]
    price_guarantee_expires_at: Optional[datetime]
    requires_instant_payment: bool

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            payment_required_by=get_and_transform(
                json, "payment_required_by", parse_datetime
            ),
            price_guarantee_expires_at=get_and_transform(
                json,
                "price_guarantee_expires_at",
                lambda value: datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ"),
            ),
            requires_instant_payment=json["requires_instant_payment"],
        )


@dataclass
class ServiceMetadata:
    """An object containing metadata about the service, like the maximum weight
    and dimensions of the baggage.
    """

    # Baggage
    type: Optional[str]
    maximum_weight_kg: Optional[int]
    maximum_height_cm: Optional[int]
    maximum_length_cm: Optional[int]
    maximum_depth_cm: Optional[int]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            type=json.get("type"),
            maximum_weight_kg=json.get("maximum_weight_kg"),
            maximum_height_cm=json.get("maximum_height_cm"),
            maximum_length_cm=json.get("maximum_length_cm"),
            maximum_depth_cm=json.get("maximum_depth_cm"),
        )


@dataclass
class Service:
    """The services that can be booked with the offer but are not included by default,
    for example an additional checked bag. This field is only returned in the [Get single
    offer](https://duffel.com/docs/api/offers/get-offer-by-id) endpoint. When there are no
    services available, or we don't support services for the airline, this list will be
    empty. If you want to know which airlines we support services for, please get in touch
    with the Duffel support team at help@duffel.com.
    """

    id: str
    maximum_quantity: int
    metadata: ServiceMetadata
    passenger_ids: Sequence[str]
    segment_ids: Sequence[str]
    total_amount: str
    total_currency: str
    type: str

    allowed_types = ["baggage"]

    class InvalidType(Exception):
        """Invalid service type"""

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            maximum_quantity=json["maximum_quantity"],
            metadata=ServiceMetadata.from_json(json["metadata"]),
            passenger_ids=json["passenger_ids"],
            segment_ids=json["segment_ids"],
            total_amount=json["total_amount"],
            total_currency=json["total_currency"],
            type=json["type"],
        )


@dataclass
class OfferSliceSegmentPassengerBaggage:
    """The baggage allowances for the passenger on this segment included in the offer.
    Some airlines may allow additional baggage to be booked as a service - see the offer's
    `available_services`
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
class OfferSliceSegmentPassenger:
    """Additional segment-specific information about the passengers included in the offer
    (e.g. their baggage allowance and the cabin class they will be travelling in)

    """

    baggages: Sequence[OfferSliceSegmentPassengerBaggage]
    cabin_class: str
    cabin_class_marketing_name: str
    passenger_id: str
    fare_basis_code: Optional[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            baggages=get_and_transform(
                json,
                "baggages",
                lambda value: [
                    OfferSliceSegmentPassengerBaggage.from_json(baggage)
                    for baggage in value
                ],
                [],
            ),
            cabin_class=json["cabin_class"],
            cabin_class_marketing_name=json["cabin_class_marketing_name"],
            passenger_id=json["passenger_id"],
            fare_basis_code=json.get("fare"),
        )


@dataclass
class OfferSliceSegment:
    """The segments - that is, specific flights - that the airline is offering
    to get the passengers from the `origin` to the `destination`
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
    passengers: Sequence[OfferSliceSegmentPassenger]

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
                    OfferSliceSegmentPassenger.from_json(passenger)
                    for passenger in value
                ],
                [],
            ),
        )


@dataclass
class OfferSliceConditionsChangeBeforeDeparture:
    """Whether this slice can be changed before the departure.

    If the slice can be changed for all of the passengers then
    the `allowed` property will be `true` and information will be
    provided about any penalties.

    If none of the passengers on the slice can be changed then
    the `allowed` property will be `false`.

    In all other cases this property will be `null` indicating we
    can't provide the information for this slice.

    The `penalty_amount` is specific to changing this slice and may not be
    the penalty that is applied if the entire offer is changed.
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
class OfferSliceConditions:
    """The conditions associated with this slice, describing the kinds of
    modifications you can make post-booking and any penalties that
    will apply to those modifications.

    This condition is applied only to this slice and to all the passengers
    associated with this offer - for information at the offer level
    (e.g. "what happens if I want to change all the slices?") refer to the
    `conditions` at the top level.

    If a particular kind of modification is allowed, you may not always be able to take
    action through the Duffel API. In some cases, you may need to contact the Duffel
    support team or the airline directly.
    """

    change_before_departure: Optional[OfferSliceConditionsChangeBeforeDeparture]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            change_before_departure=get_and_transform(
                json,
                "change_before_departure",
                OfferSliceConditionsChangeBeforeDeparture.from_json,
            ),
        )


@dataclass
class OfferSlice:
    """Each slice will include one or more segments, the specific flights that the airline
    is offering to take the passengers from the slice's origin to its destination.
    """

    id: str
    destination: Place
    destination_terminal: Optional[str]
    origin: Place
    origin_terminal: Optional[str]
    duration: Optional[str]
    fare_brand_name: Optional[str]
    segments: Sequence[OfferSliceSegment]
    conditions: OfferSliceConditions

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            destination=Place.from_json(json["destination"]),
            destination_terminal=json.get("destination_terminal"),
            origin=Place.from_json(json["origin"]),
            origin_terminal=json.get("origin_terminal"),
            duration=json.get("duration"),
            fare_brand_name=json.get("fare_brand_name"),
            segments=get_and_transform(
                json,
                "segments",
                lambda value: [
                    OfferSliceSegment.from_json(segment) for segment in value
                ],
                [],
            ),
            conditions=OfferSliceConditions.from_json(json["conditions"]),
        )


@dataclass
class OfferPassenger:
    """The passenger travelling"""

    id: str
    age: int
    type: str
    given_name: Optional[str]
    family_name: Optional[str]
    loyalty_programme_accounts: Sequence[LoyaltyProgrammeAccount]

    allowed_types = ["adult"]

    class InvalidType(Exception):
        """Invalid passenger type provided"""

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            age=json["age"],
            type=json["type"],
            given_name=json.get("given_name"),
            family_name=json.get("family_name"),
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
class Offer:
    """After you've searched for flights by creating an offer request, we'll send your
    search to a range of airlines, which may return offers.

    Each offer represents flights you can buy from an airline at a particular price that
    meet your search criteria.

    You'll see slices inside the offers. Each slice will also include a list of one or
    more specific flights (called segments) that the airline is offering to get the
    passengers where they want to go.
    """

    id: str
    live_mode: bool
    allowed_passenger_identity_document_types: Sequence[str]
    available_services: Sequence[Service]
    base_amount: str
    base_currency: str
    conditions: OfferConditions
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    owner: Airline
    partial: bool
    passenger_identity_documents_required: bool
    passengers: Sequence[OfferPassenger]
    payment_requirements: PaymentRequirements
    slices: Sequence[OfferSlice]
    tax_amount: Optional[str]
    tax_currency: Optional[str]
    total_emissions_kg: str
    total_amount: str
    total_currency: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            live_mode=json["live_mode"],
            allowed_passenger_identity_document_types=json[
                "allowed_passenger_identity_document_types"
            ],
            available_services=get_and_transform(
                json,
                "available_services",
                lambda value: [Service.from_json(passenger) for passenger in value],
                [],
            ),
            base_amount=json["base_amount"],
            base_currency=json["base_currency"],
            conditions=OfferConditions.from_json(json["conditions"]),
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            updated_at=datetime.strptime(json["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            expires_at=parse_datetime(json["expires_at"]),
            owner=Airline.from_json(json["owner"]),
            partial=json["partial"],
            passenger_identity_documents_required=json[
                "passenger_identity_documents_required"
            ],
            passengers=get_and_transform(
                json,
                "passengers",
                lambda value: [
                    OfferPassenger.from_json(passenger) for passenger in value
                ],
                [],
            ),
            payment_requirements=PaymentRequirements.from_json(
                json["payment_requirements"]
            ),
            slices=get_and_transform(
                json,
                "slices",
                lambda value: [OfferSlice.from_json(slice) for slice in value],
                [],
            ),
            tax_amount=json.get("tax_amount"),
            tax_currency=json.get("tax_currency"),
            total_amount=json["total_amount"],
            total_currency=json["total_currency"],
            total_emissions_kg=json["total_emissions_kg"],
        )
