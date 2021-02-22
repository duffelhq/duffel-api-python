class Airport:
    """Airports are used to identify origins and destinations in journey slices"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "city" and value:
                setattr(self, key, City(value))
            else:
                setattr(self, key, value)


class City:
    """The metropolitan area where the airport is located.
    Only present for airports which are registered with IATA as
    belonging to a metropolitan area.
    """

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])
