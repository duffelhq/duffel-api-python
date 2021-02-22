from ..http_client import HttpClient
from ..models import Payment


class PaymentClient(HttpClient):
    """Client to interact with Payments"""

    class InvalidPayment(Exception):
        """Invalid payment data provided"""

    class InvalidPaymentType(Exception):
        """Invalid payment type provided"""

    def __init__(self, **kwargs):
        self._url = '/air/payments'
        super().__init__(**kwargs)

    def create(self, order_id, payment):
        """POST /air/payments"""
        if set(payment.keys()) != set(['amount', 'currency', 'type']):
            raise PaymentClient.InvalidPayment(payment)
        if payment['type'] not in ['arc_bsp_cash', 'balance']:
            raise PaymentClient.InvalidPaymentType(payment['type'])
        res = self.do_post(
            self._url,
            body={'data': {'order_id': order_id, 'payment': payment}}
        )
        return Payment(res['data'])
