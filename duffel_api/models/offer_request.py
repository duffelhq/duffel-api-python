from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Sequence, Union

from duffel_api.models import Airport, City, LoyaltyProgrammeAccount, Offer
from duffel_api.utils import get_and_transform


@dataclass
class OfferRequestSlice:
    """One-way journeys can be expressed using one slice, whereas return trips will need
    two.
    """

    destination_type: str
    destination: Union[Airport, City]
    origin_type: str
    origin: Union[Airport, City]
    departure_date: date

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""

        destination_type = json["destination_type"]
        destination = json["destination"]
        if destination_type == "airport":
            destination = Airport.from_json(destination)
        elif destination_type == "city":
            destination = City.from_json(destination)

        origin_type = json["origin_type"]
        origin = json["origin"]
        if origin_type == "airport":
            origin = Airport.from_json(origin)
        elif origin_type == "city":
            origin = City.from_json(origin)

        return cls(
            destination_type=destination_type,
            destination=destination,
            origin_type=origin_type,
            origin=origin,
            departure_date=date.fromisoformat(json["departure_date"]),
        )


@dataclass
class OfferRequestPassenger:
    """The passengers who want to travel"""

    id: str
    age: int
    type: str
    given_name: Optional[str]
    family_name: Optional[str]
    loyalty_programme_accounts: Sequence[LoyaltyProgrammeAccount]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            age=json["age"],
            type=json["type"],
            given_name=json.get("given_name"),
            family_name=json.get("family_name"),
            loyalty_programme_accounts=get_and_transform(
                json,
                "loyalty_programme_accounts",
                lambda value: [
                    LoyaltyProgrammeAccount.from_json(loyalty_programme_account)
                    for loyalty_programme_account in value
                ],
                [],
            ),
        )


@dataclass
class OfferRequest:
    """To search for flights, you'll need to create an offer request. An offer request
    describes the passengers and where and when they want to travel (in the form of a
    list of slices). It may also include additional filters (e.g. a particular cabin to
    travel in).
    """

    id: str
    live_mode: bool
    cabin_class: str
    created_at: datetime
    offers: Sequence[Offer]
    slices: Sequence[OfferRequestSlice]
    passengers: Sequence[OfferRequestPassenger]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            live_mode=json["live_mode"],
            cabin_class=json["cabin_class"],
            offers=get_and_transform(
                json,
                "offers",
                lambda value: [Offer.from_json(offer) for offer in value],
                [],
            ),
            slices=get_and_transform(
                json,
                "slices",
                lambda value: [OfferRequestSlice.from_json(slice) for slice in value],
                [],
            ),
            passengers=get_and_transform(
                json,
                "passengers",
                lambda value: [
                    OfferRequestPassenger.from_json(passenger) for passenger in value
                ],
                [],
            ),
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        )
