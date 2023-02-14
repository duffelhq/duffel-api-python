from datetime import datetime

import pytest

from duffel_api.utils import parse_datetime


def test_parse_datetime():
    assert parse_datetime("2022-11-02T12:24:52Z") == datetime(2022, 11, 2, 12, 24, 52)
    assert parse_datetime("2022-11-02T12:24:52.012Z") == datetime(
        2022, 11, 2, 12, 24, 52, 12000
    )
    with pytest.raises(
        ValueError,
        match="time data '2022-11-02T-2:24:52Z' does not match format '%Y-%m-%dT%H:%M:%SZ'",  # noqa: E501
    ):
        parse_datetime("2022-11-02T-2:24:52Z")
    with pytest.raises(
        ValueError,
        match="time data '2022-11-02T12:24:52' does not match format '%Y-%m-%dT%H:%M:%S.%fZ'",  # noqa: E501
    ):
        parse_datetime("2022-11-02T12:24:52")
