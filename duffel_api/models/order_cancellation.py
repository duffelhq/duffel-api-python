from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from duffel_api.utils import get_and_transform, parse_datetime


@dataclass
class OrderCancellation:
    """To cancel an order, you'll need to create an order cancellation,
    check the refund_amount returned, and, if you're happy to go ahead and
    cancel the order.

    The refund specified by refund_amount, if any, will be returned to your
    original payment method (i.e. your Duffel balance).
    You'll then need to refund your customer (e.g. back to their credit/debit card).
    """

    id: str
    order_id: str
    live_mode: bool
    expires_at: datetime
    refund_amount: str
    refund_currency: str
    refund_to: str
    confirmed_at: Optional[datetime]
    created_at: datetime

    allowed_refund_types = [
        "arc_bsp_cash",
        "balance",
        "card",
        "voucher",
        "awaiting_payment",
    ]

    class InvalidRefundType(Exception):
        """Invalid refund type provided"""

    def __post_init__(self):
        if self.refund_to not in OrderCancellation.allowed_refund_types:
            raise OrderCancellation.InvalidRefundType(self.refund_to)

        return self

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            order_id=json["order_id"],
            live_mode=json["live_mode"],
            expires_at=parse_datetime(json["expires_at"]),
            refund_amount=json["refund_amount"],
            refund_currency=json["refund_currency"],
            refund_to=json["refund_to"],
            confirmed_at=get_and_transform(json, "confirmed_at", parse_datetime),
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        )
