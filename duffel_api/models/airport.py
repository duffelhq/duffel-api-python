from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence

from duffel_api.utils import get_and_transform


@dataclass
class City:
    """The metropolitan area where the airport is located.
    Only present for airports which are registered with IATA as
    belonging to a metropolitan area.
    """

    id: str
    name: str
    iata_code: str
    iata_country_code: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            name=json["name"],
            iata_code=json["iata_code"],
            iata_country_code=json["iata_country_code"],
        )


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


@dataclass
class Refund:
    """A Refund allows you to refund money that you had collected from a customer with a
    Payment Intent. You're able to do partial refunds and also able to do multiple
    refunds for the same Payment Intent.
    """

    id: str
    live_mode: bool
    payment_intent_id: str
    amount: str
    currency: str
    net_amount: Optional[str]
    net_currency: Optional[str]
    status: str
    destination: str
    arrival: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            live_mode=json["live_mode"],
            payment_intent_id=json["payment_intent_id"],
            amount=json["amount"],
            currency=json["currency"],
            net_amount=json.get("net_amount"),
            net_currency=json.get("net_currency"),
            status=json["status"],
            destination=json["destination"],
            arrival=json["arrival"],
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            updated_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        )
