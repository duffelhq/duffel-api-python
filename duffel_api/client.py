from .api import AircraftClient, AirportClient, AirlineClient, OfferRequestClient, \
    OfferClient, OrderCancellationClient, OrderClient, PaymentClient, SeatMapClient


class Duffel:
    """Entry point to the Duffel library"""

    def __init__(self, **kwargs):
        self._aircraft_api = AircraftClient(**kwargs)
        self._airports_api = AirportClient(**kwargs)
        self._airlines_api = AirlineClient(**kwargs)
        self._offer_requests_api = OfferRequestClient(**kwargs)
        self._offers_api = OfferClient(**kwargs)
        self._orders_api = OrderClient(**kwargs)
        self._order_cancellations_api = OrderCancellationClient(**kwargs)
        self._payments_api = PaymentClient(**kwargs)
        self._seat_maps_api = SeatMapClient(**kwargs)

    @property
    def aircraft(self):
        return self._aircraft_api

    @property
    def airports(self):
        return self._airports_api

    @property
    def airlines(self):
        return self._airlines_api

    @property
    def offer_requests(self):
        return self._offer_requests_api

    @property
    def offers(self):
        return self._offers_api

    @property
    def orders(self):
        return self._orders_api

    @property
    def order_cancellations(self):
        return self._order_cancellations_api

    @property
    def payments(self):
        return self._payments_api

    @property
    def seat_maps(self):
        return self._seat_maps_api
