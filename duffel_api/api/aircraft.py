from ..http_client import HttpClient, Pagination
from ..models import Aircraft


class AircraftClient(HttpClient):
    def __init__(self, **kwargs):
        self._url = '/air/aircraft'
        super().__init__(**kwargs)

    def get(self, id_):
        return Aircraft(self.do_get('{}/{}'.format(self._url, id_))['data'])

    def list(self, limit=50):
        return Pagination(self, Aircraft, {'limit': limit})
