"""Auxiliary contexts for handling fixtures"""
import json
from contextlib import contextmanager

from duffel_api import Duffel


@contextmanager
def fixture(name, url_path, mock, status_code, with_response=True):
    """Yields a Duffel client instance that responds to a given `url_path` under `mock`"""
    url = "http://someaddress"
    with open("tests/fixtures/{}.json".format(name)) as fh:
        if with_response:
            response = json.loads(fh.read())
            uri = "{}/{}".format(url, url_path)
            mock(uri, complete_qs=True, json=response, status_code=status_code)
            yield Duffel(access_token="some_token", api_url=url)
        else:
            uri = "{}/{}".format(url, url_path)
            mock(uri, complete_qs=True, status_code=status_code)
            yield Duffel(access_token="some_token", api_url=url)
