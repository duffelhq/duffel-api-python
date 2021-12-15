from ..utils import maybe_parse_date_entries


class OrderChangeRequest:
    """To change an order, you'll need to create an order change request. An
    order change request describes the slices of an existing paid order that you
    want to remove and search criteria for new slices you want to add.
    """

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            setattr(self, key, value)
