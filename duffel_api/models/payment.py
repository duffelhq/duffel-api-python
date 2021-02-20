from ..utils import maybe_parse_date_entries


class Payment:
    allowed_types = ['arc_bsp_cash', 'balance']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key == 'type' and value not in Payment.allowed_types:
                raise Payment.InvalidType(value)
            setattr(self, key, value)
