"""Entry point to the library"""
from .api import (
    AircraftClient,
    AirportClient,
    AirlineClient,
    OfferRequestClient,
    OfferClient,
    OrderCancellationClient,
    OrderChangeRequestClient,
    OrderClient,
    OrderChangeClient,
    OrderChangeOfferClient,
    PartialOfferRequestClient,
    PaymentClient,
    PaymentIntentClient,
    SeatMapClient,
    WebhookClient,
)


def lazy_property(func):
    """Decorator that makes a property lazy-evaluated"""
    attr_name = "_lazy_" + func.__name__

    @property
    def _lazy_property(self):
        """Function for property lazy-evaluate decorator"""
        if not hasattr(self, attr_name):
            # The attr doesn't exist yet, so call the function (`func`) that has
            # the decorator. The result of that call is set in the attr.
            #
            # It's okay to set (read: memoise) the client as an attr since we
            # each call to the client's functions (e.g. `list`) are not
            # memoised.
            setattr(self, attr_name, func(self))

        # Get the result of the function call that was set in the attr.
        return getattr(self, attr_name)

    return _lazy_property


class Duffel:
    """Client to the entire API"""

    def __init__(self, **kwargs):
        # TODO(nlopes): I really don't like how I've built this- we shouldn't keep
        # instantiating the HttpClient through class inheritance.
        # We should (maybe!) have a singleton pattern on HttpClient and use
        # composition in all of these instead.

        # Keep this as we use it when doing the lazy-evaluation of the different
        # clients
        self._kwargs = kwargs

    @lazy_property
    def aircraft(self):
        """Aircraft API - /air/aircraft"""
        return AircraftClient(**self._kwargs)

    @lazy_property
    def airports(self):
        """Airports API - /air/airports"""
        return AirportClient(**self._kwargs)

    @lazy_property
    def airlines(self):
        """Airlines API - /air/airlines"""
        return AirlineClient(**self._kwargs)

    @lazy_property
    def offer_requests(self):
        """Offer Requests API - /air/offer_requests"""
        return OfferRequestClient(**self._kwargs)

    @lazy_property
    def offers(self):
        """Offers API - /air/offers"""
        return OfferClient(**self._kwargs)

    @lazy_property
    def orders(self):
        """Orders API - /air/orders"""
        return OrderClient(**self._kwargs)

    @lazy_property
    def order_cancellations(self):
        """Order Cancellations API - /air/order_cancellations"""
        return OrderCancellationClient(**self._kwargs)

    @lazy_property
    def order_changes(self):
        """Order Changes API - /air/order_changes"""
        return OrderChangeClient(**self._kwargs)

    @lazy_property
    def order_change_offers(self):
        """Order Change Offers API - /air/order_change_offers"""
        return OrderChangeOfferClient(**self._kwargs)

    @lazy_property
    def order_change_requests(self):
        """Order Change Requests API - /air/order_change_requests"""
        return OrderChangeRequestClient(**self._kwargs)

    @lazy_property
    def partial_offer_requests(self):
        """Partial Offer Requests API - /air/partial_offer_requests"""
        return PartialOfferRequestClient(**self._kwargs)

    @lazy_property
    def payment_intents(self):
        """Payment Intents API - /payments/payment_intents"""
        return PaymentIntentClient(**self._kwargs)

    @lazy_property
    def payments(self):
        """Payments API - /air/payments"""
        return PaymentClient(**self._kwargs)

    @lazy_property
    def seat_maps(self):
        """Seat Maps API - /air/seat_maps"""
        return SeatMapClient(**self._kwargs)

    @lazy_property
    def webhooks(self):
        """Webhooks API - /air/webhooks (Preview)"""
        return WebhookClient(**self._kwargs)
