from ..utils import maybe_parse_date_entries


class OrderCancellation:
    """To cancel an order, you'll need to create an order cancellation,
    check the refund_amount returned, and, if you're happy to go ahead and
    cancel the order.

    The refund specified by refund_amount, if any, will be returned to your
    original payment method (i.e. your Duffel balance).
    You'll then need to refund your customer (e.g. back to their credit/debit card).
    """

    allowed_refund_types = [
        "arc_bsp_cash",
        "balance",
        "card",
        "voucher",
        "awaiting_payment",
    ]

    class InvalidRefundType(Exception):
        """Invalid refund type provided"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if (
                key == "refund_to"
                and value not in OrderCancellation.allowed_refund_types
            ):
                raise OrderCancellation.InvalidRefundType(value)
            setattr(self, key, value)
