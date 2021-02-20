"""Assorted auxiliary functions"""
from datetime import datetime


def maybe_parse_date_entries(key, value):
    """Parse datetime entries, depending on the value of `key`"""
    if key in ['created_at', 'updated_at', 'expires_at',
               'pay_by', 'confirmed_at', 'cancelled_at']:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')

    if key in ['departing_at', 'arriving_at', 'departure_datetime', 'arrival_datetime']:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

    return value
