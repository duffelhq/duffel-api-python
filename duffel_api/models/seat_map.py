from dataclasses import dataclass
from typing import Optional, Sequence

from duffel_api.utils import get_and_transform


@dataclass
class SeatMapCabinRowSectionElementSeatService:
    """A seat for a passenger. If the available_services list is empty (which will be
    represented as an empty list : []), the seat is unavailable.

    For display, all seats should be displayed with the same static width.

    """

    id: str
    passenger_id: str
    total_amount: str
    total_currency: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            passenger_id=json["passenger_id"],
            total_amount=json["total_amount"],
            total_currency=json["total_currency"],
        )


@dataclass
class SeatMapCabinWings:
    """Where the wings of the aircraft are in relation to rows in the cabin.

    The numbers correspond to the indices of the first and the last row which are
    overwing. You can use this to draw a visual representation of the wings to help
    users get a better idea of what they will see outside their window.

    The indices are 0th-based and are for all rows, not just those that have seats.

    This is null when no rows of the cabin are overwing.
    """

    first_row_index: int
    last_row_index: int

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            first_row_index=json["first_row_index"],
            last_row_index=json["last_row_index"],
        )


@dataclass
class SeatMapCabinRowSectionElement:
    """The element that makes up a section"""

    type: str
    # Only for seat element
    designator: Optional[str]
    name: Optional[str]
    disclosures: Optional[Sequence[str]]
    available_services: Optional[Sequence[SeatMapCabinRowSectionElementSeatService]]

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

    def __post_init__(self):
        if self.type not in SeatMapCabinRowSectionElement.allowed_types:
            raise SeatMapCabinRowSectionElement.InvalidType(self.type)

        return self

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            type=json["type"],
            designator=json.get("designator"),
            name=json.get("name"),
            disclosures=json.get("disclosures"),
            available_services=get_and_transform(
                json,
                "available_services",
                lambda value: [
                    SeatMapCabinRowSectionElementSeatService.from_json(service)
                    for service in value
                ],
            ),
        )


@dataclass
class SeatMapCabinRowSection:
    """Each row is divided into sections by one or more aisles."""

    elements: Sequence[SeatMapCabinRowSectionElement]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            elements=get_and_transform(
                json,
                "elements",
                lambda value: [
                    SeatMapCabinRowSectionElement.from_json(element)
                    for element in value
                ],
                [],
            ),
        )


@dataclass
class SeatMapCabinRow:
    """Row sections are broken up by aisles. Rows are ordered from front to back of the
    aircraft.
    """

    sections: Sequence[SeatMapCabinRowSection]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            sections=get_and_transform(
                json,
                "sections",
                lambda value: [
                    SeatMapCabinRowSection.from_json(section) for section in value
                ],
                [],
            ),
        )


@dataclass
class SeatMapCabin:
    """Cabins are ordered by deck from lowest to highest, and then within each deck from
    the front to back of the aircraft.
    """

    cabin_class: str
    deck: int
    wings: Optional[SeatMapCabinWings]
    aisles: int
    rows: Sequence[SeatMapCabinRow]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            cabin_class=json["cabin_class"],
            deck=json["deck"],
            wings=get_and_transform(json, "wings", SeatMapCabinWings.from_json),
            aisles=json["aisles"],
            rows=get_and_transform(
                json,
                "rows",
                lambda value: [SeatMapCabinRow.from_json(row) for row in value],
                [],
            ),
        )


@dataclass
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

    id: str
    slice_id: str
    segment_id: str
    cabins: Sequence[SeatMapCabin]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            slice_id=json["slice_id"],
            segment_id=json["segment_id"],
            cabins=get_and_transform(
                json,
                "cabins",
                lambda value: [SeatMapCabin.from_json(cabin) for cabin in value],
                [],
            ),
        )
