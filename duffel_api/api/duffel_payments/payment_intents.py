from ...http_client import HttpClient
from ...models import PaymentIntent


class PaymentIntentClient(HttpClient):
    """To begin the process of collecting a card payment from your customer, you
    need to create a Payment Intent.

    The Payment Intent will contain a client_token that you use to collect the
    card payment in your application.

    If the Payment Intent is created in test mode you should use a test card.
    """

    def __init__(self, **kwargs):
        self._url = "/payments/payment_intents"
        super().__init__(**kwargs)

    def create(self):
        """Initiate creation of a Payment Intent"""
        return PaymentIntentCreate(self)

    def get(self, id_):
        """Get a single Payment Intent.

        You should use this API to get the complete, up-to-date information
        about a Payment Intent.
        """
        res = self.do_get(f"{self._url}/{id_}")
        if res is not None:
            return PaymentIntent.from_json(res["data"])

    def confirm(self, id_):
        """Confirm a Payment Intent

        Once you've successfully collected the customer's card details, using
        the client_token from when you first created the Payment Intent, you
        then need to confirm it using this endpoint.

        Once confirmed, the amount charged to your customer's card will be added
        to your Balance (minus any Duffel Payment fees).
        """
        res = self.do_post(f"{self._url}/{id_}/actions/confirm")
        if res is not None:
            return PaymentIntent.from_json(res["data"])


class PaymentIntentCreate:
    """Auxiliary class to provide methods for creating payment intents"""

    class InvalidPayment(Exception):
        """Invalid payment data provided"""

    def __init__(self, client):
        self._client = client
        self._amount = None
        self._currency = None

    @staticmethod
    def _validate_payment_keys(payment_details):
        """Validate that payment keys are correct"""
        if set(payment_details.keys()) != set(["amount", "currency"]):
            raise PaymentIntentCreate.InvalidPayment(payment_details)

    def payment(self, payment_details):
        """Set amount and currency"""
        PaymentIntentCreate._validate_payment_keys(payment_details)

        self._amount = payment_details["amount"]
        self._currency = payment_details["currency"]

        return self

    def execute(self):
        """POST /payments/payment_intents"""
        if self._amount is None:
            raise PaymentIntentCreate.InvalidPayment()

        if self._currency is None:
            raise PaymentIntentCreate.InvalidPayment()

        res = self._client.do_post(
            self._client._url,
            body={
                "data": {
                    "amount": self._amount,
                    "currency": self._currency,
                }
            },
        )
        return PaymentIntent.from_json(res["data"])
