from ..http_client import HttpClient, Pagination
from ..models import Airport


class AirportClient(HttpClient):
    def __init__(self, **kwargs):
        self._url = '/air/airports'
        super().__init__(**kwargs)

    def get(self, id_):
        return Airport(self.do_get('{}/{}'.format(self._url, id_))['data'])

    def list(self, limit=50):
        return Pagination(self, Airport, {'limit': limit})
