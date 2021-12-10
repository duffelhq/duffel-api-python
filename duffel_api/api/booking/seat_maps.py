from ...http_client import HttpClient
from ...models import SeatMap


class SeatMapClient(HttpClient):
    """Client to interact with Seat Maps"""

    def __init__(self, **kwargs):
        self._url = "/air/seat_maps"
        super().__init__(**kwargs)

    def get(self, offer_id):
        """GET /air/seat_maps"""
        data = self.do_get(self._url, query_params={"offer_id": offer_id})["data"]
        return [SeatMap(m) for m in data]
