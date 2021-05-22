from ..models import (
    Airline,
    Place,
    Aircraft,
    OfferConditionChangeBeforeDeparture,
    OfferConditionRefundBeforeDeparture,
)
from ..utils import maybe_parse_date_entries


class Order:
    """Once you've searched for flights by creating an offer request, and you've chosen
    which offer you want to book, you'll then want to create an order.

    To create an order, you just need to provide the offer ID, payment details and some
    additional information on the passengers (e.g. their full name and date of birth).

    """

    def __init__(self, json):
        for key in json:
            value = json[key]
            if value is not None:
                value = maybe_parse_date_entries(key, json[key])
            if key == "documents":
                value = [OrderDocument(v) for v in value]
            elif key == "conditions":
                value = OrderConditions(value)
            elif key == "owner":
                value = Airline(value)
            elif key == "passengers":
                value = [OrderPassenger(v) for v in value]
            elif key == "payment_status":
                value = OrderPaymentStatus(value)
            elif key == "services":
                value = [OrderService(v) for v in value]
            elif key == "slices":
                value = [OrderSlice(v) for v in value]
            setattr(self, key, value)


class OrderConditions:
    """The conditions associated with this order, describing the kinds of modifications you
    can make to it and any penalties that will apply to those modifications. This
    information assumes the condition is applied to all of the slices and passengers
    associated with this order - for information at the slice level (e.g. "what happens if
    I just want to change the first slice?") refer to the slices. If a particular kind of
    modification is allowed, you may not always be able to take action through the Duffel
    API. In some cases, you may need to contact the Duffel support team or the airline
    directly.

    """

    def __init__(self, json):
        for key in json:
            if key == "change_before_departure":
                value = OrderConditionChangeBeforeDeparture(json[key])
            elif key == "refund_before_departure":
                value = OrderConditionRefundBeforeDeparture(json[key])
            setattr(self, key, value)


OrderConditionChangeBeforeDeparture = OfferConditionChangeBeforeDeparture
OrderConditionRefundBeforeDeparture = OfferConditionRefundBeforeDeparture


class OrderSlice:
    """A slice is one part of the slices that make up the itinerary of an order.
    One-way journeys can be expressed using one slice, whereas return trips will need two.

    """

    allowed_place_types = ["airport", "city"]

    class InvalidPlaceType(Exception):
        """Invalid type of place provided"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key in ["destination", "origin"]:
                value = Place(value)
            elif key in ["destination_type", "origin_type"]:
                if value not in OrderSlice.allowed_place_types:
                    raise OrderSlice.InvalidPlaceType(value)
            elif key == "segments":
                value = [OrderSliceSegment(v) for v in value]
            # TODO(nlopes): maybe convert duration to a timedelta or Duration
            setattr(self, key, value)


class OrderSliceSegment:
    """The segments - that is, specific flights - that the airline is offering to get the
    passengers from the `origin` to the `destination`

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
                value = [OrderSliceSegmentPassenger(p) for p in value]
            setattr(self, key, value)


class OrderSliceSegmentPassenger:
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
                value = [OrderSliceSegmentPassengerBaggage(v) for v in value]
            elif key == "seat":
                value = OrderSliceSegmentPassengerSeat(value)
            elif key == "cabin_class":
                if value not in OrderSliceSegmentPassenger.allowed_cabin_classes:
                    raise OrderSliceSegmentPassenger.InvalidCabinClass(value)
            setattr(self, key, value)


class OrderSliceSegmentPassengerSeat:
    """An object containing metadata about the service, like the designator of the seat"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            setattr(self, key, value)


# TODO(nlopes): maybe this can be strictly equivalent to OfferSliceSegmentPassengerBaggage
class OrderSliceSegmentPassengerBaggage:
    """The baggage allowances for the passenger on this segment that were included in the
    original offer. Any extra baggage items which were booked as services will be listed
    in the services field instead of here.

    """

    allowed_types = ["checked", "carry_on"]

    class InvalidType(Exception):
        """Invalid baggage type"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if (
                key == "type"
                and value not in OrderSliceSegmentPassengerBaggage.allowed_types
            ):
                raise OrderSliceSegmentPassengerBaggage.InvalidType(value)
            setattr(self, key, value)


class OrderService:
    """The service booked along with this order"""

    allowed_types = ["baggage", "seat"]

    class InvalidType(Exception):
        """Invalid service type"""

    def __init__(self, json):
        service_type = json["type"]
        if service_type not in OrderService.allowed_types:
            raise OrderService.InvalidType(service_type)

        for key in json:
            value = json[key]
            if key == "metadata":
                if service_type == "baggage":
                    value = OrderServiceMetadataBaggage(value)
                elif service_type == "seat":
                    value = OrderServiceMetadataSeat(value)
            setattr(self, key, value)


class OrderServiceMetadataSeat:
    """An object containing metadata about the service, like the designator of the seat"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            setattr(self, key, value)


class OrderServiceMetadataBaggage:
    """An object containing metadata about the service, like the maximum weight and
    dimensions of the baggage.

    """

    allowed_types = ["checked", "carry_on"]

    class InvalidType(Exception):
        """Invalid baggage type"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "type" and value not in OrderServiceMetadataBaggage.allowed_types:
                raise OrderServiceMetadataBaggage.InvalidType(value)
            setattr(self, key, value)


class OrderPaymentStatus:
    """The payment status for an order"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if value is not None:
                value = maybe_parse_date_entries(key, json[key])
            setattr(self, key, value)


class OrderPassenger:
    """A passenger who is travelling"""

    allowed_genders = ["m", "f"]
    allowed_types = ["adult", "child", "infant_without_seat"]
    allowed_titles = ["mr", "mrs", "ms", "miss"]

    class InvalidGender(Exception):
        """Invalid passenger gender"""

    class InvalidTitle(Exception):
        """Invalid passenger title"""

    class InvalidType(Exception):
        """Invalid passenger type"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key == "gender" and value.lower() not in OrderPassenger.allowed_genders:
                raise OrderPassenger.InvalidGender(value)
            elif key == "title" and value.lower() not in OrderPassenger.allowed_titles:
                raise OrderPassenger.InvalidTitle(value)
            elif key == "type" and value.lower() not in OrderPassenger.allowed_types:
                raise OrderPassenger.InvalidType(value)
            setattr(self, key, value)


class OrderDocument:
    """A document issued for this order."""

    allowed_types = [
        "electronic_ticket",
        "electronic_miscellaneous_document_associated",
        "electronic_miscellaneous_document_standalone",
    ]

    class InvalidType(Exception):
        """Invalid document type"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "type" and value not in OrderDocument.allowed_types:
                raise OrderDocument.InvalidType(value)
            setattr(self, key, value)
