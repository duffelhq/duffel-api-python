from ...http_client import HttpClient, Pagination
from ...models import Airport


class AirportClient(HttpClient):
    """Client to interact with Airports"""

    def __init__(self, **kwargs):
        self._url = "/air/airports"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/airports/:id"""
        return Airport(self.do_get("{}/{}".format(self._url, id_))["data"])

    def list(self, limit=50):
        """GET /air/airports"""
        return Pagination(self, Airport, {"limit": limit})
