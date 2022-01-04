"""Assorted auxiliary functions"""
from datetime import date, datetime
from typing import Any, Union


def maybe_parse_date_entries(key: str, value: Any) -> Union[str, datetime, date]:
    """Parse appropriate datetime or date entries, depending on the value of `key`"""
    if not isinstance(value, str):
        # If it's not a string, don't attempt any parsing
        return value
    if key in [
        "created_at",
        "updated_at",
        "pay_by",
        "cancelled_at",
    ]:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

    if key in [
        "price_guarantee_expires_at",
        "payment_required_by",
        "synced_at",
    ]:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")

    if key in [
        "departing_at",
        "arriving_at",
        "departure_datetime",
        "arrival_datetime",
    ]:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")

    if key in ["departure_date", "born_on"]:
        # Once we no longer support python 3.6 we can replace these two lines with:
        # date.fromisoformat(value)
        t = datetime.strptime(value, "%Y-%m-%d")
        return date(t.year, t.month, t.day)

    if key in ["confirmed_at", "expires_at"]:
        # There are inconsistent formats used for this field depending on the
        # endpoint
        if len(value) == 20:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        else:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

    # All other strings
    return value


def version():
    """Return the version specified in the package (setup.py) during runtime"""
    import pkg_resources

    return pkg_resources.require("duffel_api")[0].version
