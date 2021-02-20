from ..http_client import HttpClient, Pagination
from ..models import Airline


class AirlineClient(HttpClient):
    def __init__(self, **kwargs):
        self._url = '/air/airlines'
        super().__init__(**kwargs)

    def get(self, id_):
        return Airline(self.do_get('{}/{}'.format(self._url, id_))['data'])

    def list(self, limit=50):
        return Pagination(self, Airline, {'limit': limit})
