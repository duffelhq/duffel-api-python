"""Auxiliary contexts for handling fixtures"""
from contextlib import contextmanager
import json

from duffel_api import Duffel


@contextmanager
def fixture(name, url_path, mock):
    """Yields a Duffel client instance that responds to a given `url_path` under `mock`)"""
    url = "http://someaddress"
    with open("tests/fixtures/{}.json".format(name)) as fh:
        response = json.loads(fh.read())
        uri = "{}/air{}".format(url, url_path)
        mock(uri, complete_qs=True, json=response)
        yield Duffel(api_token="some_token", url=url)
