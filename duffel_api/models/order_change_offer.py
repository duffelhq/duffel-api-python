from ..models import Place
from ..utils import maybe_parse_date_entries


class OrderChangeOffer:
    """After you've searched for flights to add to your order by creating an order change
    request, we'll send your search to a range of airlines, which may return order change
    offers.

    Each order change offer represents flights you can buy from an airline at a particular
    price that meets your search criteria.

    You'll see slices inside the offers. Each slice will also include a list of one or
    more specific flights (called segments) that the airline is offering to get the
    passengers where they want to go.

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
                and value not in OrderChangeOffer.allowed_refund_types
            ):
                raise OrderChangeOffer.InvalidRefundType(value)
            if key == "slices":
                value = OrderChangeOfferSlices(value)
            setattr(self, key, value)


class OrderChangeOfferSlices:
    """The slices to be added and/or removed"""

    def __init__(self, json):
        add = list(map(lambda add: OrderChangeOfferSlicesAdd(add), json["add"]))
        remove = list(
            map(lambda remove: OrderChangeOfferSlicesRemove(remove), json["remove"])
        )

        setattr(self, "add", add)
        setattr(self, "remove", remove)


class OrderChangeOfferSlicesAdd:
    allowed_place_types = ["airport", "city"]

    class InvalidPlaceType(Exception):
        """Invalid type of place"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key in ["destination", "origin"]:
                value = Place(value)
            elif key in ["destination_type", "origin_type"]:
                if value not in OrderChangeOfferSlicesAdd.allowed_place_types:
                    raise OrderChangeOfferSlicesAdd.InvalidPlaceType(value)
            # TODO(nlopes): maybe convert duration to a timedelta or Duration
            setattr(self, key, value)


OrderChangeOfferSlicesRemove = OrderChangeOfferSlicesAdd
