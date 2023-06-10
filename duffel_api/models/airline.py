from dataclasses import dataclass
from typing import Optional


@dataclass
class Airline:
    """Airlines are used to identify the air travel companies selling and operating
    flights
    """

    id: str
    name: str
    iata_code: Optional[str]
    logo_lockup_url: Optional[str]
    logo_symbol_url: Optional[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            name=json["name"],
            iata_code=json.get("iata_code"),
            logo_lockup_url=json.get("logo_lockup_url"),
            logo_symbol_url=json.get("logo_symbol_url"),
        )
