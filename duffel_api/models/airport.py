from dataclasses import dataclass
from typing import Optional

from duffel_api.models import City
from duffel_api.utils import get_and_transform


@dataclass
class Airport:
    """Airports are used to identify origins and destinations in journey
    slices"""

    id: str
    name: str
    iata_code: Optional[str]
    icao_code: Optional[str]
    iata_country_code: str
    latitude: float
    longitude: float
    time_zone: str
    city: Optional[City]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            name=json["name"],
            iata_code=json.get("iata_code"),
            icao_code=json.get("icao_code"),
            iata_country_code=json["iata_country_code"],
            latitude=json["latitude"],
            longitude=json["longitude"],
            time_zone=json["time_zone"],
            city=get_and_transform(json, "city", City.from_json),
        )
