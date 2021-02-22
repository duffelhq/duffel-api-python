class SeatMap:
    """Seat maps are used to build a rich experience for your customers so they can select
    a seat as part of an order.

    A seat map includes the data for rendering seats in the relevant cabins, along with
    their total cost and other information such as disclosures.

    A seat is a special kind of service in that they're not shown when getting an
    individual offer with return_available_services set to true. They're only available
    through this endpoint.

    So far we support selecting seats when you create an order. This means we do not
    support selecting a seat after an order has already been created or cancelling a
    booked seat.

    Display recommendations
    =======================

    Each seat, empty, and bassinet element should be displayed with the same static width,
    while other elements should ideally fill or shrink in the available space in the
    section. However, displaying them with a static width could also be appropriate.

    If these elements don't fill the whole section, they should be displayed as
    middle-aligned by default.

    """

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "cabins":
                value = [SeatMapCabin(v) for v in value]
            setattr(self, key, value)


class SeatMapCabin:
    """Cabins are ordered by deck from lowest to highest, and then within each deck from
    the front to back of the aircraft.

    """

    allowed_classes = ["first", "business", "premium_economy", "economy"]

    class InvalidClass(Exception):
        """Invalid seat map cabin class provided"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "cabin_class" and value not in SeatMapCabin.allowed_classes:
                raise SeatMapCabin.InvalidClass(value)
            elif key == "wings" and value:
                value = SeatMapCabinWings(value)
            elif key == "rows":
                value = [SeatMapCabinRow(r) for r in value]
            setattr(self, key, value)


class SeatMapCabinRow:
    """Row sections are broken up by aisles. Rows are ordered from front to back of the
    aircraft.

    """

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "sections":
                value = [SeatMapCabinRowSection(s) for s in value]
            setattr(self, key, value)


class SeatMapCabinRowSection:
    """Each row is divided into sections by one or more aisles."""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "elements":
                value = [SeatMapCabinRowSectionElement(s) for s in value]
            setattr(self, key, value)


class SeatMapCabinRowSectionElement:
    """The element that makes up a section"""

    allowed_types = [
        "seat",
        "bassinet",
        "empty",
        "exit_row",
        "lavatory",
        "galley",
        "closet",
        "stairs",
    ]

    class InvalidType(Exception):
        """Invalid seat map cabin row section element provided"""

    def __init__(self, json):
        element_type = json["type"]
        if element_type not in SeatMapCabinRowSectionElement.allowed_types:
            raise SeatMapCabinRowSectionElement.InvalidType(element_type)

        if element_type == "seat":
            for key in json:
                value = json[key]
                if key == "available_services":
                    value = [SeatMapCabinRowSectionElementSeatService(s) for s in value]
                setattr(self, key, value)
        else:
            setattr(self, "type", element_type)


class SeatMapCabinRowSectionElementSeatService:
    """A seat for a passenger. If the available_services list is empty (which will be
    represented as an empty list : []), the seat is unavailable.

    For display, all seats should be displayed with the same static width.

    """

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])


class SeatMapCabinWings:
    """Where the wings of the aircraft are in relation to rows in the cabin.

    The numbers correspond to the indices of the first and the last row which are
    overwing. You can use this to draw a visual representation of the wings to help
    users get a better idea of what they will see outside their window.

    The indices are 0th-based and are for all rows, not just those that have seats.

    This is null when no rows of the cabin are overwing.

    """

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])
