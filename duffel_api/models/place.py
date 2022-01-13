from dataclasses import dataclass
from typing import Optional, Sequence

from duffel_api.models import Airport, City
from duffel_api.utils import get_and_transform


@dataclass
class Place:
    """The city or airport"""

    id: str
    name: str
    type: str
    iata_city_code: Optional[str]
    iata_country_code: str
    latitude: Optional[float]
    longitude: Optional[float]
    icao_code: Optional[str]
    time_zone: Optional[str]
    city_name: Optional[str]
    city: Optional[City]
    airports: Optional[Sequence[Airport]]

    allowed_types = ["airport", "city"]

    class InvalidType(Exception):
        """Invalid type of place"""

    def __post_init__(self):
        if self.type not in Place.allowed_types:
            raise Place.InvalidType(self.type)

        return self

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            name=json["name"],
            type=json["type"],
            iata_city_code=json.get("iata_city_code"),
            iata_country_code=json["iata_country_code"],
            latitude=json.get("latitude"),
            longitude=json.get("longitude"),
            icao_code=json.get("icao_code"),
            time_zone=json.get("time_zone"),
            city_name=json.get("city_name"),
            city=get_and_transform(json, "city", City.from_json),
            airports=get_and_transform(
                json,
                "airports",
                lambda value: [Airport.from_json(airport) for airport in value],
            ),
        )
