from ..models import Airport, City, Offer, Passenger
from ..utils import maybe_parse_date_entries


class OfferRequest:
    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key == 'offers':
                value = [Offer(v) for v in value]
            elif key == 'passengers':
                value = [Passenger(v) for v in value]
            elif key == 'slices':
                value = [Slice(v) for v in value]
            setattr(self, key, value)


class Slice:
    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key in ['destination', 'origin']:
                place_type = json['{}_type'.format(key)]
                if place_type == 'airport':
                    value = Airport(value)
                elif place_type == 'city':
                    value = City(value)
            setattr(self, key, value)
