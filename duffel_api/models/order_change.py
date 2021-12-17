from ..models import Place
from ..utils import maybe_parse_date_entries


class OrderChange:
    """Once you've created an order change request, and you've chosen which
    slices to add and remove, you'll then want to create an order change.

    To create an order change, you just need to provide the order change offer
    ID.

    If change_total_amount is greater than zero, you will need to provide
    payment details when confirming the change.

    If change_total_amount is less than zero, this amount will be returned to
    the payment method specified by refund_to.

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
            if key == "refund_to" and value not in OrderChange.allowed_refund_types:
                raise OrderChange.InvalidRefundType(value)
            if key == "slices":
                value = OrderChangeSlices(value)
            setattr(self, key, value)


class OrderChangeSlices:
    """The slices to be added and/or removed"""

    def __init__(self, json):
        add = list(map(lambda add: OrderChangeSlicesAdd(add), json["add"]))
        remove = list(
            map(lambda remove: OrderChangeSlicesRemove(remove), json["remove"])
        )

        setattr(self, "add", add)
        setattr(self, "remove", remove)


class OrderChangeSlicesAdd:
    allowed_place_types = ["airport", "city"]

    class InvalidPlaceType(Exception):
        """Invalid type of place"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key in ["destination", "origin"]:
                value = Place(value)
            elif key in ["destination_type", "origin_type"]:
                if value not in OrderChangeSlicesAdd.allowed_place_types:
                    raise OrderChangeSlicesAdd.InvalidPlaceType(value)
            # TODO(nlopes): maybe convert duration to a timedelta or Duration
            setattr(self, key, value)


OrderChangeSlicesRemove = OrderChangeSlicesAdd
