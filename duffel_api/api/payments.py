from ..http_client import HttpClient
from ..models import Payment


class PaymentClient(HttpClient):
    class InvalidPayment(Exception):
        pass

    class InvalidPaymentType(Exception):
        pass

    def __init__(self, **kwargs):
        self._url = '/air/payments'
        super().__init__(**kwargs)

    def create(self, order_id, payment):
        if set(payment.keys()) != set(['amount', 'currency', 'type']):
            raise PaymentClient.InvalidPayment(payment)
        if payment['type'] not in ['arc_bsp_cash', 'balance']:
            raise PaymentClient.InvalidPaymentType(payment['type'])
        res = self.do_post(
            self._url,
            body={'data': {'order_id': order_id, 'payment': payment}}
        )
        return Payment(res['data'])
