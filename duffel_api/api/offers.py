from ..http_client import HttpClient, Pagination
from ..models import Offer


class OfferClient(HttpClient):
    """Client to interact with Offers"""

    def __init__(self, **kwargs):
        self._url = "/air/offers"
        super().__init__(**kwargs)

    def get(self, id_, return_available_services=False):
        """GET /air/offers/:id"""
        params = {}
        if return_available_services:
            params["return_available_services"] = "true"
        return Offer(
            self.do_get("{}/{}".format(self._url, id_), query_params=params)[
                "data"
            ]
        )

    def list(
        self, offer_request_id, sort=None, max_connections=None, limit=50
    ):
        """GET /air/offers"""
        params = {"limit": limit, "offer_request_id": offer_request_id}
        if sort:
            params["sort"] = sort
        if max_connections:
            params["max_connections"] = max_connections
        return Pagination(self, Offer, params)
