from ..utils import maybe_parse_date_entries


class Webhook:
    """
    Webhooks are used to automatically receive notifications of events that
    happen. For example, when an order has a schedule change.
    """

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            setattr(self, key, value)
