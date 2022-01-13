from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Payment:
    """To pay for an unpaid order you've previously created, you'll need to create a
    payment for it.

    The payment details you provide will be charged and, if successful, your order will
    be confirmed with the airline.

    """

    id: str
    live_mode: bool
    type: str
    amount: str
    currency: Optional[str]
    created_at: datetime

    allowed_types = ["arc_bsp_cash", "balance"]

    class InvalidType(Exception):
        """Invalid payment type provided"""

    def __post_init__(self):
        if self.type not in Payment.allowed_types:
            raise Payment.InvalidType(self.type)

        return self

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            type=json["type"],
            live_mode=json["live_mode"],
            amount=json["amount"],
            currency=json.get("currency"),
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        )
