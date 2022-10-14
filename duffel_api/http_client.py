"""Http Client, api response and error management"""
import os

from requests import Request, Session
from requests import codes as http_codes

from .utils import version


class ClientError(Exception):
    """An error originated from the client"""


class ApiError(Exception):
    """An error originated from the API"""

    def __init__(self, headers, json):
        self._headers = headers
        self.meta = json["meta"]
        self.errors = json["errors"]
        # We always only print the first error message
        self.message = self.errors[0]["message"]
        super().__init__(self.message)

    def __str__(self):
        """Custom message for our API errors"""
        err = self.errors[0]
        return f"{err['type']}: {err['title']}: {self.message}"

    @property
    def headers(self):
        """Request headers"""
        return self._headers


# TODO(nlopes): I don't like this. Pagination in this way means the user will be
# constrained by this flow.  A better way would be to return a ListObject that contains
# the first list of objects and then if the user wants auto pagination, they can call
# something like `auto_paginate` or something along those lines.  We also don't provide
# good mechanisms for the user to react to rate limiting when auto paginating.
class Pagination:
    """A way to do pagination on list() calls"""

    def __init__(self, client, caller, params):
        self._client = client
        self._caller = caller

        if params["limit"] > 200:
            # We're vaguely faking the structure of the error structure returned
            # from the API.
            raise ApiError([], {"errors": [{"message": "limit exceeds 200"}]})
        self._params = params

    def __iter__(self):
        """Iterate over the response items and yield one by one"""
        response = self._client.do_get(
            self._client._url,
            query_params=self._params,
        )

        while "meta" in response:
            after = response["meta"]["after"]
            for entry in response["data"]:
                yield self._caller.from_json(entry)

            if after is None:
                break

            self._params["after"] = after
            response = self._client.do_get(
                self._client._url,
                query_params=self._params,
            )


class HttpClient:
    """Http Client to manage all calls to the Duffel API"""

    URL = "https://api.duffel.com"
    VERSION = "v1"

    def __init__(self, access_token=None, api_url=None, api_version=None, **settings):
        if api_url is not None:
            self._api_url = api_url
        else:
            self._api_url = HttpClient.URL
        if api_version is not None:
            self._api_version = api_version
        else:
            self._api_version = HttpClient.VERSION

        self.http_session = Session()
        self._settings = settings

        user_agent = f"Duffel/{self._api_version} duffel_api_python/{version()}"
        self.http_session.headers.update({"User-Agent": user_agent})
        self.http_session.headers.update({"Accept": "application/json"})
        self.http_session.headers.update({"Duffel-Version": self._api_version})
        if not access_token:
            access_token = os.getenv("DUFFEL_ACCESS_TOKEN")
            if not access_token:
                raise ClientError("must set DUFFEL_ACCESS_TOKEN")
        self.http_session.headers.update({"Authorization": f"Bearer {access_token}"})

    def _http_call(self, endpoint, method, query_params=None, body=None):
        """Perform the http call and wrap the response in a ApiError in case an error
        occurred

        """
        request_url = self._api_url + endpoint
        request = Request(method, request_url, params=query_params, json=body)
        prepared = self.http_session.prepare_request(request)
        response = self.http_session.send(prepared, **self._settings)
        if response.status_code in [
            http_codes.ok,
            http_codes.created,
        ]:
            try:
                return response.json()
            except ValueError as err:
                raise Exception(f"something bad happened: {response.text}") from err
        elif response.status_code == http_codes.no_content:
            return None
        else:
            try:
                raise ApiError(response.headers, response.json())
            except ValueError as err:
                raise Exception(f"something bad happened: {response.text}") from err
            raise response.raise_for_status()

    def do_get(self, endpoint, method="GET", query_params=None, body=None):
        """Issue a GET request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)

    def do_post(self, endpoint, method="POST", query_params=None, body=None):
        """Issue a POST request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)

    def do_delete(self, endpoint, method="DELETE", query_params=None, body=None):
        """Issue a DELETE request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)

    def do_put(self, endpoint, method="PUT", query_params=None, body=None):
        """Issue a PUT request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)

    def do_patch(self, endpoint, method="PATCH", query_params=None, body=None):
        """Issue a PATCH request to `endpoint`"""
        return self._http_call(endpoint, method, query_params, body)
