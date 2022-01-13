from dataclasses import dataclass
from datetime import date, datetime
from typing import Sequence

from duffel_api.models import OrderChangeOffer
from duffel_api.utils import get_and_transform


@dataclass
class OrderChangeRequestSliceAdd:
    """The slice to be added"""

    cabin_class: str
    departure_date: date
    destination: str
    origin: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            cabin_class=json["cabin_class"],
            departure_date=date.fromisoformat(json["departure_date"]),
            destination=json["destination"],
            origin=json["origin"],
        )


@dataclass
class OrderChangeRequestSliceRemove:
    """The slice to be removed"""

    slice_id: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            slice_id=json["slice_id"],
        )


@dataclass
class OrderChangeRequestSlices:
    """The slices to be added and/or removed"""

    add: Sequence[OrderChangeRequestSliceAdd]
    remove: Sequence[OrderChangeRequestSliceRemove]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            add=get_and_transform(
                json,
                "add",
                lambda value: [
                    OrderChangeRequestSliceAdd.from_json(slice) for slice in value
                ],
                [],
            ),
            remove=get_and_transform(
                json,
                "remove",
                lambda value: [
                    OrderChangeRequestSliceRemove.from_json(slice) for slice in value
                ],
                [],
            ),
        )


@dataclass
class OrderChangeRequest:
    """To change an order, you'll need to create an order change request. An
    order change request describes the slices of an existing paid order that you
    want to remove and search criteria for new slices you want to add.
    """

    id: str
    live_mode: bool
    created_at: datetime
    updated_at: datetime
    order_id: str
    slices: OrderChangeRequestSlices
    order_change_offers: Sequence[OrderChangeOffer]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            live_mode=json["live_mode"],
            order_id=json["order_id"],
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            updated_at=datetime.strptime(json["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            slices=OrderChangeRequestSlices.from_json(json["slices"]),
            order_change_offers=get_and_transform(
                json,
                "order_change_offers",
                lambda value: [
                    OrderChangeOffer.from_json(order_change_offer)
                    for order_change_offer in value
                ],
                [],
            ),
        )
