from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
