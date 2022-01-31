from dataclasses import dataclass


@dataclass
class Aircraft:
    """Aircraft are used to describe what passengers will fly in for a given trip"""

    id: str
    iata_code: str
    name: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            iata_code=json["iata_code"],
            name=json["name"],
        )
