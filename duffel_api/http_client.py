"""Http Client, api response and error management"""
import os
from requests import Session, Request, codes as http_codes

from .utils import version


class ClientError(Exception):
    """An error originated from the client"""


class ApiError(Exception):
    """An error originated from the API"""

    def __init__(self, json, message=None):
        self.meta = json['meta']
        self.errors = json['errors']
        # We always only print the first error message
        self.message = self.errors[0]['message']
        super().__init__(self.message)

    def __str__(self):
        err = self.errors[0]
        return f"{err['type']}: {err['title']}: {self.message}"


class Pagination:
    """A way to do pagination on list() calls"""

    def __init__(self, client, caller, params):
        self._client = client
        self._caller = caller

        if params['limit'] > 200:
            raise ApiError('limit exceeds 200')
        self._params = params

    def __iter__(self):
        response = self._client.do_get(
            self._client._url,
            query_params=self._params,
        )

        while 'meta' in response:
            after = response['meta']['after']
            for entry in response['data']:
                yield self._caller(entry)

            if after is None:
                break

            self._params['after'] = after
            response = self._client.do_get(
                self._client._url,
                query_params=self._params,
            )


class HttpClient:
    """Http Client to manage all calls to the Duffel API"""
    URL = 'https://api.duffel.com'
    VERSION = 'beta'

    def __init__(self, api_token=None, url=None):
        if url is not None:
            HttpClient.URL = url
        self.http_session = Session()

        user_agent = f'Duffel/{HttpClient.VERSION} duffel_api_python/{version()}'
        self.http_session.headers.update({'User-Agent': user_agent})
        self.http_session.headers.update({'Duffel-Version': HttpClient.VERSION})

        if not api_token:
            api_token = os.getenv('DUFFEL_API_TOKEN')
            if not api_token:
                raise ClientError('must set DUFFEL_API_TOKEN')
            self.http_session.headers.update(
                {'Authorization': 'Bearer {}'.format(api_token)}
            )

    def _http_call(self, endpoint, method, query_params=None, body=None):
        request_url = HttpClient.URL + endpoint
        request = Request(method, request_url, params=query_params, json=body)
        prepared = self.http_session.prepare_request(request)
        # TODO(nlopes): WE MUST HAVE TIMEOUTS, TIMEOUTS!
        response = self.http_session.send(prepared)
        if response.status_code in [
                http_codes.ok,
                http_codes.created,
                http_codes.no_content]:
            try:
                return response.json()
            except ValueError as err:
                raise Exception('something bad happened: {}'.format(
                    response.text)) from err
        else:
            try:
                raise ApiError(response.json())
            except ValueError as err:
                raise Exception('something bad happened: {}'.format(
                    response.text)) from err
            raise response.raise_for_status()

    def do_get(self, endpoint, method='GET', query_params=None, body=None):
        """Issue a GET request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)

    def do_post(self, endpoint, method='POST', query_params=None, body=None):
        """Issue a POST request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)

    def do_delete(self, endpoint, method='DELETE', query_params=None,
                  body=None):
        """Issue a DELETE request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)

    def do_put(self, endpoint, method='PUT', query_params=None, body=None):
        """Issue a PUT request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)
