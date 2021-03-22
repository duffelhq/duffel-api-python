class Webhook:
    """Webhooks are used to automatically receive notifications of events that happen. For example, when an order has a schedule change.

    """
    def __init__(self, json):
        for key in json:
            value = json[key]
            setattr(self, key, value)
