from dataclasses import dataclass


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
