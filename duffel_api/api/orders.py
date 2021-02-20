from ..http_client import HttpClient, Pagination
from ..models import Order


class OrderClient(HttpClient):
    """TODO"""

    class InvalidSort(Exception):
        pass

    def __init__(self, **kwargs):
        self._url = '/air/orders'
        super().__init__(**kwargs)

    def get(self, id_):
        return Order(self.do_get('{}/{}'.format(self._url, id_))['data'])

    def list(self, awaiting_payment=False, sort=None, limit=50):
        params = {'limit': limit}
        if sort:
            if sort not in ['pay_by', '-pay_by']:
                raise OrderClient.InvalidSort(sort)
            params['sort'] = sort
        if awaiting_payment:
            params['awaiting_payment'] = 'true'
        return Pagination(self, Order, params)

    def create(self):
        return OrderCreate(self)


class OrderCreate:
    class InvalidSelectedOffersLength(Exception):
        pass

    class InvalidService(Exception):
        pass

    class InvalidNumberOfPayments(Exception):
        pass

    class InvalidPayment(Exception):
        pass

    class InvalidPaymentType(Exception):
        pass

    class InvalidNumberOfPassengers(Exception):
        pass

    class InvalidPassenger(Exception):
        pass

    def __init__(self, client):
        self._client = client
        self._passengers = []
        self._payments = []
        self._selected_offers = []
        self._services = []
        self._payment_type = 'instant'

    def _validate_payments(payments):
        if len(payments) == 0:
            raise OrderCreate.InvalidNumberOfPayments(len(payments))
        for payment in payments:
            if set(payment.keys()) != set(['amount', 'currency', 'type']):
                raise OrderCreate.InvalidPayment(payment)
            if payment['type'] not in ['arc_bsp_cash', 'balance']:
                raise OrderCreate.InvalidPaymentType(payment['type'])

    def _validate_services(services):
        for service in services:
            if set(service.keys()) != set(['id', 'quantity']):
                raise OrderCreate.InvalidService(service)

    def _validate_selected_offers(selected_offers):
        if len(selected_offers) != 1:
            raise OrderCreate.InvalidSelectedOffersLength(len(selected_offers))

    def _validate_passengers(passengers):
        if len(passengers) == 0:
            raise OrderCreate.InvalidNumberOfPassengers(passengers)
        for passenger in passengers:
            if not ('born_on' in passenger or 'email' in passenger or
                    'family_name' in passenger or 'gender' in passenger or
                    'given_name' in passenger or 'id' in passenger or
                    'phone_number' in passenger or 'title' in passenger):
                raise OrderCreate.InvalidPassenger(passenger)

    def pay_later(self):
        """Set payment type to 'pay_later'. If this isn't called the type is 'instant'"""
        self._payment_type = 'pay_later'
        return self

    def selected_offers(self, selected_offers):
        OrderCreate._validate_selected_offers(selected_offers)
        self._selected_offers = selected_offers
        return self

    def services(self, services):
        # TODO(nlopes): this should be its own type to ensure the user *only* passes valid
        # data
        OrderCreate._validate_services(services)
        self._services = services
        return self

    def payments(self, payments):
        # TODO(nlopes): this should be its own type to ensure the user *only* passes valid
        # data
        OrderCreate._validate_payments(payments)
        self._payments = payments
        return self

    def passengers(self, passengers):
        # TODO(nlopes): this should be its own type to ensure the user *only* passes valid
        # data
        OrderCreate._validate_passengers(passengers)
        self._passengers = passengers
        return self

    def execute(self):
        OrderCreate._validate_passengers(self._passengers)
        OrderCreate._validate_payments(self._payments)
        OrderCreate._validate_services(self._services)
        OrderCreate._validate_selected_offers(self._selected_offers)
        res = self._client.do_post(
            self._client._url,
            body={'data': {'type': self._payment_type,
                           'passengers': self._passengers,
                           'services': self._services,
                           'selected_offers': self._selected_offers,
                           'payments': self._payments}}
        )
        return Order(res['data'])
