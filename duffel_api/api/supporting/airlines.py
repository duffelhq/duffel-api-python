from ...http_client import HttpClient, Pagination
from ...models import Airline


class AirlineClient(HttpClient):
    """Client to interact with Airlines"""

    def __init__(self, **kwargs):
        self._url = "/air/airlines"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/airlines/:id"""
        res = self.do_get(f"{self._url}/{id_}")
        if res is not None:
            return Airline.from_json(res["data"])

    def list(self, limit=50):
        """GET /air/airlines"""
        return Pagination(self, Airline, {"limit": limit})
