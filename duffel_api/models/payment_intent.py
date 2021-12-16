from ..utils import maybe_parse_date_entries


class PaymentIntent:
    """To begin the process of collecting a card payment from your customer, you
    need to create a Payment Intent.

    The Payment Intent will contain a client_token that you use to collect the
    card payment in your application.

    If the Payment Intent is created in test mode you should use a test card.
    """

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            setattr(self, key, value)
