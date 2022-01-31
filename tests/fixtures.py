"""Auxiliary contexts for handling fixtures"""
import json
from contextlib import contextmanager

from duffel_api import Duffel


@contextmanager
def fixture(name, url_path, mock, status_code, with_response=True):
    """Yields a Duffel client instnace.

    It responds to a given `url_path` under `mock`."""
    url = "http://someaddress"
    with open(f"tests/fixtures/{name}.json") as fh:
        if with_response:
            response = json.loads(fh.read())
            uri = f"{url}/{url_path}"
            mock(uri, complete_qs=True, json=response, status_code=status_code)
            yield Duffel(access_token="some_token", api_url=url)
        else:
            uri = f"{url}/{url_path}"
            mock(uri, complete_qs=True, status_code=status_code)
            yield Duffel(access_token="some_token", api_url=url)


@contextmanager
def raw_fixture(name):
    """Yields an instance of the fixture that has been loaded as JSON."""
    with open(f"tests/fixtures/{name}.json") as fh:
        yield json.load(fh)
