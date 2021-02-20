from datetime import date

from ..models import Airline, Place, Aircraft
from ..utils import maybe_parse_date_entries


class Order:
    def __init__(self, json):
        for key in json:
            value = json[key]
            if value is not None:
                value = maybe_parse_date_entries(key, json[key])
            if key == 'documents':
                value = [OrderDocument(v) for v in value]
            elif key == 'owner':
                value = Airline(value)
            elif key == 'passengers':
                value = [OrderPassenger(v) for v in value]
            elif key == 'payment_status':
                value = OrderPaymentStatus(value)
            elif key == 'services':
                value = [OrderService(v) for v in value]
            elif key == 'slices':
                value = [OrderSlice(v) for v in value]
            setattr(self, key, value)


class OrderSlice:
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
                if value not in OrderSlice.allowed_place_types:
                    raise OrderSlice.InvalidPlaceType(value)
            elif key == 'segments':
                value = [OrderSliceSegment(v) for v in value]
            # TODO(nlopes): maybe convert duration to a timedelta or Duration
            setattr(self, key, value)


class OrderSliceSegment:
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
                value = [OrderSliceSegmentPassenger(p) for p in value]
            setattr(self, key, value)


class OrderSliceSegmentPassenger:
    """Additional segment-specific information about the passengers included in the offer
    (e.g. their baggage allowance and the cabin class they will be travelling in)
    """
    allowed_cabin_classes = ['economy', 'premium_economy', 'business', 'first']

    class InvalidCabinClass(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'baggages':
                value = [OrderSliceSegmentPassengerBaggage(v) for v in value]
            elif key == 'seat':
                value = OrderSliceSegmentPassengerSeat(value)
            elif key == 'cabin_class':
                if value not in OrderSliceSegmentPassenger.allowed_cabin_classes:
                    raise OrderSliceSegmentPassenger.InvalidCabinClass(value)
            setattr(self, key, value)


class OrderSliceSegmentPassengerSeat:
    """An object containing metadata about the service, like the designator of the seat.
    """

    def __init__(self, json):
        for key in json:
            value = json[key]
            setattr(self, key, value)


# TODO(nlopes): maybe this can be strictly equivalent to OfferSliceSegmentPassengerBaggage
class OrderSliceSegmentPassengerBaggage:
    allowed_types = ['checked', 'carry_on']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'type' and \
               value not in OrderSliceSegmentPassengerBaggage.allowed_types:
                raise OrderSliceSegmentPassengerBaggage.InvalidType(value)
            setattr(self, key, value)


class OrderService:
    allowed_types = ['baggage', 'seat']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        service_type = json['type']
        if service_type not in OrderService.allowed_types:
            raise OrderService.InvalidType(service_type)

        for key in json:
            value = json[key]
            if key == 'metadata':
                if service_type == 'baggage':
                    value = OrderServiceMetadataBaggage(value)
                elif service_type == 'seat':
                    value = OrderServiceMetadataSeat(value)
            setattr(self, key, value)


class OrderServiceMetadataSeat:
    def __init__(self, json):
        for key in json:
            value = json[key]
            setattr(self, key, value)


class OrderServiceMetadataBaggage:
    allowed_types = ['checked', 'carry_on']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'type' and value not in OrderServiceMetadataBaggage.allowed_types:
                raise OrderServiceMetadataBaggage.InvalidType(value)
            setattr(self, key, value)


class OrderPaymentStatus:
    def __init__(self, json):
        for key in json:
            value = json[key]
            if value is not None:
                value = maybe_parse_date_entries(key, json[key])
            setattr(self, key, value)


class OrderPassenger:
    allowed_genders = ['m', 'f']
    allowed_types = ['adult', 'child', 'infant_without_seat']
    allowed_titles = ['mr', 'mrs', 'ms', 'miss']

    class InvalidGender(Exception):
        pass

    class InvalidTitle(Exception):
        pass

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'born_on':
                value = date.fromisoformat(value)
            elif key == 'gender' and value.lower() not in OrderPassenger.allowed_genders:
                raise OrderPassenger.InvalidGender(value)
            elif key == 'title' and value.lower() not in OrderPassenger.allowed_titles:
                raise OrderPassenger.InvalidTitle(value)
            elif key == 'type' and value.lower() not in OrderPassenger.allowed_types:
                raise OrderPassenger.InvalidType(value)
            setattr(self, key, value)


class OrderDocument:
    allowed_types = [
        'electronic_ticket',
        'electronic_miscellaneous_document_associated',
        'electronic_miscellaneous_document_standalone',
    ]

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'type' and value not in OrderDocument.allowed_types:
                raise OrderDocument.InvalidType(value)
            setattr(self, key, value)
