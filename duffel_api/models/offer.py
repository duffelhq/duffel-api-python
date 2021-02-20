from datetime import date

from ..models import Aircraft, Airline, Passenger, Place
from ..utils import maybe_parse_date_entries


class Offer:
    allowed_passenger_identity_document_types = ['passport']

    class InvalidPassengerIdentityDocumentType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key == 'allowed_passenger_identity_document_types':
                Offer._validate_passenger_types(value)
            elif key == 'slices':
                value = [OfferSlice(v) for v in value]
            elif key == 'passengers':
                value = [Passenger(v) for v in value]
            elif key == 'payment_requirements':
                value = PaymentRequirements(value)
            elif key == 'available_services':
                value = [Service(v) for v in value]
            elif key == 'owner':
                value = Airline(value)
            setattr(self, key, value)

    def _validate_passenger_types(document_types):
        for doc_type in document_types:
            if doc_type not in Offer.allowed_passenger_identity_document_types:
                raise Offer.InvalidPassengerIdentityDocumentType(document_types)


class PaymentRequirements:
    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            setattr(self, key, value)


class Service:
    allowed_types = ['baggage']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'metadata':
                value = ServiceMetadata(value)
            if key == 'type' and value not in Service.allowed_types:
                raise Service.InvalidType(value)
            setattr(self, key, value)


class ServiceMetadata:
    """An object containing metadata about the service, like the maximum weight
    and dimensions of the baggage.
    """

    allowed_types = ['checked', 'carry_on']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'type' and value not in ServiceMetadata.allowed_types:
                raise ServiceMetadata.InvalidType(value)
            setattr(self, key, value)


class OfferSlice:
    """Each slice will include one or more segments, the specific flights that
    the airline is offering to take the passengers from the slice's origin to
    its destination.
    """

    allowed_place_types = ['airport', 'city']

    class InvalidPlaceType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'departure_date':
                value = date.fromisoformat(value)
            elif key in ['destination', 'origin']:
                value = Place(value)
            elif key in ['destination_type', 'origin_type']:
                if value not in OfferSlice.allowed_place_types:
                    raise OfferSlice.InvalidPlaceType(value)
            elif key == 'segments':
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
            if key == 'aircraft' and value:
                value = Aircraft(value)
            elif key in ['marketing_carrier', 'operating_carrier'] and value:
                value = Airline(value)
            elif key in ['destination', 'origin']:
                value = Place(value)
            elif key == 'passengers':
                value = [OfferSliceSegmentPassenger(p) for p in value]
            setattr(self, key, value)


class OfferSliceSegmentPassenger:
    allowed_cabin_classes = ['economy', 'premium_economy', 'business', 'first']

    class InvalidCabinClass(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'baggages':
                value = [OfferSliceSegmentPassengerBaggage(v) for v in value]
            elif key == 'cabin_class':
                if value not in OfferSliceSegmentPassenger.allowed_cabin_classes:
                    raise OfferSliceSegmentPassenger.InvalidCabinClass(value)
            setattr(self, key, value)


class OfferSliceSegmentPassengerBaggage:
    """The baggage allowances for the passenger on this segment included in the offer.
    Some airlines may allow additional baggage to be booked as a service - see the offer's
    `available_services`
    """

    allowed_types = ['checked', 'carry_on']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'type' and \
               value not in OfferSliceSegmentPassengerBaggage.allowed_types:
                raise OfferSliceSegmentPassengerBaggage.InvalidType(value)
            setattr(self, key, value)
