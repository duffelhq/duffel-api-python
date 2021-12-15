from ...http_client import HttpClient, Pagination
from ...models import PaymentIntent


class PaymentIntentClient(HttpClient):
    """To begin the process of collecting a card payment from your customer, you need to create a Payment Intent.

    The Payment Intent will contain a client_token that you use to collect the card payment in your application.

    If the Payment Intent is created in test mode you should use a test card.
    """

    def __init__(self, **kwargs):
        self._url = "/payments/payment_intents"
        super().__init__(**kwargs)

    def create(self):
        """Initiate creation of a Payment Intent"""
        return PaymentIntentCreate(self)


class PaymentIntentCreate:
    """Auxiliary class to provide methods for creating payment intents"""

    class InvalidPayment(Exception):
        """Invalid payment data provided"""

    def __init__(self, client):
        self._client = client
        self._amount = None
        self._currency = None

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
        if self._amount == None:
            raise PaymentIntentCreate.InvalidPayment(payment_details)

        if self._currency == None:
            raise PaymentIntentCreate.InvalidPayment(payment_details)

        res = self._client.do_post(
                self._client._url,
                body={
                    "data": {
                        "amount": self._amount,
                        "currency": self._currency,
                        }
                    }
                )
        return PaymentIntent(res["data"])

