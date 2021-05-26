from ..utils import maybe_parse_date_entries


class Payment:
    """To pay for an unpaid order you've previously created, you'll need to create a
    payment for it.

    The payment details you provide will be charged and, if successful, your order will
    be confirmed with the airline.

    """

    allowed_types = ["arc_bsp_cash", "balance", "payments"]

    class InvalidType(Exception):
        """Invalid payment type provided"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key == "type" and value not in Payment.allowed_types:
                raise Payment.InvalidType(value)
            setattr(self, key, value)
