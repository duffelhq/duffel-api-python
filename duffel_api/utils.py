"""Assorted auxiliary functions"""
from datetime import datetime
from typing import Any


def identity(value: Any) -> Any:
    """Given a value, return the exact same value"""
    return value


def get_and_transform(dict: dict, key: str, fn, default=None):
    """Get a value from a dictionary and transform it or return
    None if the key isn't present"""
    try:
        value = dict[key]
        if value is None:
            return value
        else:
            return fn(value)
    except KeyError:
        return default


def version() -> str:
    """Return the version specified in the package (setup.py) during runtime"""
    import pkg_resources

    return pkg_resources.require("duffel_api")[0].version


def parse_datetime(value: str) -> datetime:
    """Parse a datetime string regardless of having milliseconds or not"""
    # There are inconsistent formats used for the field, therefore we try to accomodate
    # instead of making an API breaking change.
    if len(value) == 20:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    else:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
