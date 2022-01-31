from ...http_client import HttpClient
from ...models import Payment


class PaymentClient(HttpClient):
    """Client to interact with Payments."""

    class InvalidPayment(Exception):
        """Invalid payment data provided"""

    class InvalidPaymentType(Exception):
        """Invalid payment type provided"""

    def __init__(self, **kwargs):
        self._url = "/air/payments"
        super().__init__(**kwargs)

    def create(self):
        """Initiate creation of a Payment."""
        return PaymentCreate(self)


class PaymentCreate:
    """Auxiliary class to provide methods for payment creation related data"""

    def __init__(self, client):
        self._client = client
        self._order_id = None
        self._payment = None

    @staticmethod
    def _validate_payment(payment):
        """Validate payment details"""
        if set(payment.keys()) != set(["amount", "currency", "type"]):
            raise PaymentClient.InvalidPayment(payment)
        if payment["type"] not in ["arc_bsp_cash", "balance", "payments"]:
            raise PaymentClient.InvalidPaymentType(payment["type"])

    def order(self, order_id):
        """Add order identifier"""
        self._order_id = order_id
        return self

    def payment(self, payment):
        """Add payment details"""
        self._payment = payment
        return self

    def execute(self):
        """POST /air/payments."""
        PaymentCreate._validate_payment(self._payment)
        res = self._client.do_post(
            self._client._url,
            body={"data": {"order_id": self._order_id, "payment": self._payment}},
        )
        return Payment.from_json(res["data"])
