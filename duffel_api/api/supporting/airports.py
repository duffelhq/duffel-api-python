from ...http_client import HttpClient, Pagination
from ...models import Airport


class AirportClient(HttpClient):
    """Client to interact with Airports"""

    def __init__(self, **kwargs):
        self._url = "/air/airports"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/airports/:id"""
        res = self.do_get(f"{self._url}/{id_}")
        if res is not None:
            return Airport.from_json(res["data"])

    def list(self, limit=50):
        """GET /air/airports"""
        return Pagination(self, Airport, {"limit": limit})
