from ...http_client import HttpClient, Pagination
from ...models import Aircraft


class AircraftClient(HttpClient):
    """Client to interact with Aircraft"""

    def __init__(self, **kwargs):
        self._url = "/air/aircraft"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/aircraft/:id"""
        res = self.do_get(f"{self._url}/{id_}")
        if res is not None:
            return Aircraft.from_json(res["data"])

    def list(self, limit=50):
        """GET /air/aircraft"""
        return Pagination(self, Aircraft, {"limit": limit})
