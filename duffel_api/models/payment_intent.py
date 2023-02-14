from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence

from duffel_api.models import Refund
from duffel_api.utils import get_and_transform, parse_datetime


@dataclass
class PaymentIntent:
    """To begin the process of collecting a card payment from your customer, you
    need to create a Payment Intent.

    The Payment Intent will contain a client_token that you use to collect the
    card payment in your application.

    If the Payment Intent is created in test mode you should use a test card.
    """

    id: str
    live_mode: bool
    amount: str
    currency: str
    net_amount: Optional[str]
    net_currency: Optional[str]
    fees_amount: Optional[str]
    fees_currency: Optional[str]
    client_token: str
    card_network: Optional[str]
    card_last_four_digits: Optional[str]
    card_country_code: Optional[str]
    status: str
    refunds: Sequence[Refund]
    confirmed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            live_mode=json["live_mode"],
            amount=json["amount"],
            currency=json["currency"],
            net_amount=json.get("net_amount"),
            net_currency=json.get("net_currency"),
            fees_amount=json.get("fees_amount"),
            fees_currency=json.get("fees_currency"),
            client_token=json["client_token"],
            card_network=json.get("card_network"),
            card_last_four_digits=json.get("card_last_four_digits"),
            card_country_code=json.get("card_country_code"),
            status=json["status"],
            refunds=get_and_transform(
                json,
                "refunds",
                lambda value: [Refund.from_json(refund) for refund in value],
                [],
            ),
            confirmed_at=get_and_transform(json, "confirmed_at", parse_datetime),
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            updated_at=datetime.strptime(json["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        )
