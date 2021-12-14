from ..models import Aircraft, Airline, Passenger, Place
from ..utils import maybe_parse_date_entries


class Offer:
    """After you've searched for flights by creating an offer request, we'll send your
    search to a range of airlines, which may return offers.

    Each offer represents flights you can buy from an airline at a particular price that
    meet your search criteria.

    You'll see slices inside the offers. Each slice will also include a list of one or
    more specific flights (called segments) that the airline is offering to get the
    passengers where they want to go.

    """

    allowed_passenger_identity_document_types = ["passport"]

    class InvalidPassengerIdentityDocumentType(Exception):
        """Invalid passenger identity document type"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key == "allowed_passenger_identity_document_types":
                Offer._validate_passenger_identity_document_types(value)
            elif key == "conditions":
                value = OfferConditions(value)
            elif key == "slices":
                value = [OfferSlice(v) for v in value]
            elif key == "passengers":
                value = [Passenger(v) for v in value]
            elif key == "payment_requirements":
                value = PaymentRequirements(value)
            elif key == "available_services":
                value = [Service(v) for v in value]
            elif key == "owner":
                value = Airline(value)
            setattr(self, key, value)

    @staticmethod
    def _validate_passenger_identity_document_types(document_types):
        """Validate passenger identity document types"""
        for doc_type in document_types:
            if doc_type not in Offer.allowed_passenger_identity_document_types:
                raise Offer.InvalidPassengerIdentityDocumentType(document_types)


class OfferConditions:
    """The conditions associated with this offer, describing the kinds of modifications you
    can make post-booking and any penalties that will apply to those modifications.

    """

    def __init__(self, json):
        for key in json:
            if key == "change_before_departure":
                value = OfferConditionChangeBeforeDeparture(json[key])
            elif key == "refund_before_departure":
                value = OfferConditionRefundBeforeDeparture(json[key])
            setattr(self, key, value)


class OfferConditionChangeBeforeDeparture:
    """Whether the whole offer can be changed before the departure of the first slice. If all
    of the slices on the offer can be changed then the allowed property will be
    true. Refer to the slices for information about change penalties. If any of the slices
    on the offer can't be changed then the allowed property will be false. In this case
    you should refer to the slices conditions to determine if any part of the offer is
    changeable. If the airline hasn't provided any information about whether this offer
    can be changed then this property will be null.

    """

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])


class OfferConditionRefundBeforeDeparture:
    """Whether the whole offer can be refunded before the departure of the first slice.

    If all of the slices on the offer can be refunded then the allowed property will be
    true and information will be provided about any penalties. If any of the slices on the
    offer can't be refunded then the allowed property will be false. If the airline hasn't
    provided any information about whether this offer can be refunded then this property
    will be null.

    """

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])


class PaymentRequirements:

    """The payment requirements for an offer"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            setattr(self, key, value)


class Service:
    """The services that can be booked along with the offer but are not included by default,
    for example an additional checked bag. This field is only returned in the [Get single
    offer](https://duffel.com/docs/api/offers/get-offer-by-id) endpoint. When there are no
    services available, or we don't support services for the airline, this list will be
    empty. If you want to know which airlines we support services for, please get in touch
    with the Duffel support team at help@duffel.com.

    """

    allowed_types = ["baggage"]

    class InvalidType(Exception):
        """Invalid service type"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "metadata":
                value = ServiceMetadata(value)
            if key == "type" and value not in Service.allowed_types:
                raise Service.InvalidType(value)
            setattr(self, key, value)


class ServiceMetadata:
    """An object containing metadata about the service, like the maximum weight
    and dimensions of the baggage.
    """

    allowed_types = ["checked", "carry_on"]

    class InvalidType(Exception):
        """Invalid service metadata type for baggage"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "type" and value not in ServiceMetadata.allowed_types:
                raise ServiceMetadata.InvalidType(value)
            setattr(self, key, value)


class OfferSlice:
    """Each slice will include one or more segments, the specific flights that the airline is
    offering to take the passengers from the slice's origin to its destination.

    """

    allowed_place_types = ["airport", "city"]

    class InvalidPlaceType(Exception):
        """Invalid type of place"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key in ["destination", "origin"]:
                value = Place(value)
            elif key in ["destination_type", "origin_type"]:
                if value not in OfferSlice.allowed_place_types:
                    raise OfferSlice.InvalidPlaceType(value)
            elif key == "segments":
                value = [OfferSliceSegment(v) for v in value]
            # TODO(nlopes): maybe convert duration to a timedelta or Duration
            setattr(self, key, value)


class OfferSliceSegment:
    """The segments - that is, specific flights - that the airline is offering
    to get the passengers from the `origin` to the `destination`
    """

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key == "aircraft" and value:
                value = Aircraft(value)
            elif key in ["marketing_carrier", "operating_carrier"] and value:
                value = Airline(value)
            elif key in ["destination", "origin"]:
                value = Place(value)
            elif key == "passengers":
                value = [OfferSliceSegmentPassenger(p) for p in value]
            setattr(self, key, value)


class OfferSliceSegmentPassenger:
    """Additional segment-specific information about the passengers included in the offer
    (e.g. their baggage allowance and the cabin class they will be travelling in)

    """

    allowed_cabin_classes = ["economy", "premium_economy", "business", "first"]

    class InvalidCabinClass(Exception):
        """Invalid cabin class"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "baggages":
                value = [OfferSliceSegmentPassengerBaggage(v) for v in value]
            elif key == "cabin_class":
                if value not in OfferSliceSegmentPassenger.allowed_cabin_classes:
                    raise OfferSliceSegmentPassenger.InvalidCabinClass(value)
            setattr(self, key, value)


class OfferSliceSegmentPassengerBaggage:
    """The baggage allowances for the passenger on this segment included in the offer.
    Some airlines may allow additional baggage to be booked as a service - see the offer's
    `available_services`
    """

    allowed_types = ["checked", "carry_on"]

    class InvalidType(Exception):
        """Invalid baggage type"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if (
                key == "type"
                and value not in OfferSliceSegmentPassengerBaggage.allowed_types
            ):
                raise OfferSliceSegmentPassengerBaggage.InvalidType(value)
            setattr(self, key, value)
