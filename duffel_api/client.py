from .api import AircraftClient, AirportClient, AirlineClient, OfferRequestClient, \
    OfferClient, OrderCancellationClient, OrderClient, PaymentClient, SeatMapClient


class Duffel:
    """Entry point to the Duffel library"""

    def __init__(self, **kwargs):
        # TODO(nlopes): I really don't like how I've built this- we shouldn't keep
        # instantiating the HttpClient through class inheritance.
        # We should (maybe!) have a singleton pattern on HttpClient and use
        # composition in all of these instead.
        self._kwargs = kwargs

    @property
    def aircraft(self):
        if not hasattr(self, 'aircraft_client'):
            setattr(self, 'aircraft_client', AircraftClient(**self._kwargs))
        return self.aircraft_client

    @property
    def airports(self):
        if not hasattr(self, 'airport_client'):
            setattr(self, 'airport_client', AirportClient(**self._kwargs))
        return self.airport_client

    @property
    def airlines(self):
        if not hasattr(self, 'airline_client'):
            setattr(self, 'airline_client', AirlineClient(**self._kwargs))
        return self.airline_client

    @property
    def offer_requests(self):
        if not hasattr(self, 'offer_request_client'):
            setattr(self, 'offer_request_client', OfferRequestClient(**self._kwargs))
        return self.offer_request_client

    @property
    def offers(self):
        if not hasattr(self, 'offer_client'):
            setattr(self, 'offer_client', OfferClient(**self._kwargs))
        return self.offer_client

    @property
    def orders(self):
        if not hasattr(self, 'order_client'):
            setattr(self, 'order_client', OrderClient(**self._kwargs))
        return self.order_client

    @property
    def order_cancellations(self):
        if not hasattr(self, 'order_cancellation_client'):
            setattr(self, 'order_cancellation_client',
                    OrderCancellationClient(**self._kwargs))
        return self.order_cancellation_client

    @property
    def payments(self):
        if not hasattr(self, 'payment_client'):
            setattr(self, 'payment_client', PaymentClient(**self._kwargs))
        return self.payment_client

    @property
    def seat_maps(self):
        if not hasattr(self, 'seat_map_client'):
            setattr(self, 'seat_map_client', SeatMapClient(**self._kwargs))
        return self.seat_map_client
