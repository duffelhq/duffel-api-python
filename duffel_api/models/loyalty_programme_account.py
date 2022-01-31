from dataclasses import dataclass


@dataclass
class LoyaltyProgrammeAccount:
    """A passenger's loyalty programme account"""

    airline_iata_code: str
    account_number: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            airline_iata_code=json["airline_iata_code"],
            account_number=json["account_number"],
        )
