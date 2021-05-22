from ..http_client import HttpClient, Pagination
from ..models import OrderChangeOffer


class OrderChangeOffersClient(HttpClient):
    """Client to interact with Order Change Offers"""

    def __init__(self, **kwargs):
        self._url = "/air/order_change_offers"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/order_change_offers/:id"""
        return OrderChangeOffer(self.do_get("{}/{}".format(self._url, id_))["data"])

    def list(self, order_change_request_id, sort=None, max_connections=None, limit=50):
        """GET /air/order_change_offers"""
        params = {"limit": limit, "order_change_request_id": order_change_request_id}
        if sort:
            params["sort"] = sort
        if max_connections:
            params["max_connections"] = max_connections
        return Pagination(self, OrderChangeOffer, params)
