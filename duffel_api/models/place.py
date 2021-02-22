from ..models import City


class Place:
    """The city or airport"""

    allowed_types = ["airport", "city"]

    class InvalidType(Exception):
        """Invalid type of place"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "type" and value not in Place.allowed_types:
                raise Place.InvalidType(value)
            elif key == "city" and value:
                value = City(value)
            elif key == "airports" and value:
                value = [CityAirport(v) for v in value]
            setattr(self, key, value)


class CityAirport:
    """The airport associated to a city."""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "city":
                value = City(value)
            setattr(self, key, value)
