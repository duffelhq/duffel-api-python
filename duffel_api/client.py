"""Entry point to the library"""
from .api import (
    AircraftClient,
    AirportClient,
    AirlineClient,
    OfferRequestClient,
    OfferClient,
    OrderCancellationClient,
    OrderClient,
    OrderChangeClient,
    OrderChangeOfferClient,
    PaymentClient,
    PaymentIntentClient,
    SeatMapClient,
    WebhookClient,
)


class Duffel:
    """Client to the entire API"""

    def __init__(self, **kwargs):
        # TODO(nlopes): I really don't like how I've built this- we shouldn't keep
        # instantiating the HttpClient through class inheritance.
        # We should (maybe!) have a singleton pattern on HttpClient and use
        # composition in all of these instead.
        self._kwargs = kwargs

        # Lazily initialise clients by when they're called
        self.aircraft_client = None
        self.airport_client = None
        self.airline_client = None
        self.offer_request_client = None
        self.offer_client = None
        self.order_client = None
        self.order_cancellation_client = None
        self.order_change_client = None
        self.order_change_offer_client = None
        self.payment_intent_client = None
        self.payment_client = None
        self.seat_map_client = None
        self.webhook_client = None

    @property
    def aircraft(self):
        """Aircraft API - /air/aircraft"""
        if isinstance(self.aircraft_client, type(None)):
            setattr(self, "aircraft_client", AircraftClient(**self._kwargs))
        return self.aircraft_client

    @property
    def airports(self):
        """Airports API - /air/airports"""
        if isinstance(self.airport_client, type(None)):
            setattr(self, "airport_client", AirportClient(**self._kwargs))
        return self.airport_client

    @property
    def airlines(self):
        """Airlines API - /air/airlines"""
        if isinstance(self.airline_client, type(None)):
            setattr(self, "airline_client", AirlineClient(**self._kwargs))
        return self.airline_client

    @property
    def offer_requests(self):
        """Offer Requests API - /air/offer_requests"""
        if isinstance(self.offer_request_client, type(None)):
            setattr(
                self,
                "offer_request_client",
                OfferRequestClient(**self._kwargs),
            )
        return self.offer_request_client

    @property
    def offers(self):
        """Offers API - /air/offers"""
        if isinstance(self.offer_client, type(None)):
            setattr(self, "offer_client", OfferClient(**self._kwargs))
        return self.offer_client

    @property
    def orders(self):
        """Orders API - /air/orders"""
        if isinstance(self.order_client, type(None)):
            setattr(self, "order_client", OrderClient(**self._kwargs))
        return self.order_client

    @property
    def order_cancellations(self):
        """Order Cancellations API - /air/order_cancellations"""
        if isinstance(self.order_cancellation_client, type(None)):
            setattr(
                self,
                "order_cancellation_client",
                OrderCancellationClient(**self._kwargs),
            )
        return self.order_cancellation_client

    @property
    def order_changes(self):
        """Order Changes API - /air/order_changes"""
        if isinstance(self.order_change_client, type(None)):
            setattr(
                self,
                "order_change_client",
                OrderChangeClient(**self._kwargs),
            )
        return self.order_change_client

    @property
    def order_change_offers(self):
        """Order Change Offers API - /air/order_change_offers"""
        if isinstance(self.order_change_offer_client, type(None)):
            setattr(
                self,
                "order_change_offer_client",
                OrderChangeOfferClient(**self._kwargs),
            )
        return self.order_change_offer_client

    @property
    def payment_intents(self):
        """Payment Intents API - /payments/payment_intents"""
        if isinstance(self.payment_intent_client, type(None)):
            setattr(self, "payment_intent_client", PaymentIntentClient(**self._kwargs))
        return self.payment_intent_client

    @property
    def payments(self):
        """Payments API - /air/payments"""
        if isinstance(self.payment_client, type(None)):
            setattr(self, "payment_client", PaymentClient(**self._kwargs))
        return self.payment_client

    @property
    def seat_maps(self):
        """Seat Maps API - /air/seat_maps"""
        if isinstance(self.seat_map_client, type(None)):
            setattr(self, "seat_map_client", SeatMapClient(**self._kwargs))
        return self.seat_map_client

    @property
    def webhooks(self):
        """Webhooks API - /air/webhooks (Preview)"""
        if isinstance(self.webhook_client, type(None)):
            setattr(self, "webhook_client", WebhookClient(**self._kwargs))
        return self.webhook_client
