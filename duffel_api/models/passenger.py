class Passenger:
    """The passenger travelling"""

    allowed_types = ['adult']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'type' and value and value not in Passenger.allowed_types:
                raise Passenger.InvalidType(value)
            setattr(self, key, value)
