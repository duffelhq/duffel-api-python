from typing import Any, Dict

from ...http_client import HttpClient, Pagination
from ...models import Order


class OrderClient(HttpClient):
    """Client to interact with Orders."""

    class InvalidSort(Exception):
        """Invalid sort option provided"""

    def __init__(self, **kwargs):
        """Instantiate an Order client."""
        self._url = "/air/orders"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/orders/:id."""
        res = self.do_get(f"{self._url}/{id_}")
        if res is not None:
            return Order.from_json(res["data"])

    def list(self, awaiting_payment=False, sort=None, limit=50):
        """GET /air/orders."""
        params: Dict[str, Any] = {"limit": limit}
        if sort:
            if sort not in ["pay_by", "-pay_by"]:
                raise OrderClient.InvalidSort(sort)
            params["sort"] = sort
        if awaiting_payment:
            params["awaiting_payment"] = "true"
        return Pagination(self, Order, params)

    def create(self):
        """Initiate creation of an Order."""
        return OrderCreate(self)

    def update(self, id_):
        """Initiate updating of an Order."""
        return OrderUpdate(self, id_)


class OrderCreate:
    """Auxiliary class to provide methods for order creation related data"""

    class InvalidSelectedOffersLength(Exception):
        """Invalid number of selected_offers provided"""

    class InvalidService(Exception):
        """Invalid service data provided"""

    class InvalidNumberOfPayments(Exception):
        """Invalid number of payments provided"""

    class InvalidPayment(Exception):
        """Invalid payment data provided"""

    class InvalidPaymentType(Exception):
        """Invalid payment type provided"""

    class InvalidNumberOfPassengers(Exception):
        """Invalid number of passengers provided"""

    class InvalidPassenger(Exception):
        """Invalid passenger data provided"""

    def __init__(self, client):
        self._client = client
        self._passengers = []
        self._payments = []
        self._selected_offers = []
        self._services = []
        self._payment_type = "instant"

    @staticmethod
    def _validate_payments(payments):
        """Validate number of payments and the data provided for each if any were given"""
        if len(payments) == 0:
            raise OrderCreate.InvalidNumberOfPayments(len(payments))
        for payment in payments:
            if set(payment.keys()) != set(["amount", "currency", "type"]):
                raise OrderCreate.InvalidPayment(payment)
            if payment["type"] not in ["arc_bsp_cash", "balance"]:
                raise OrderCreate.InvalidPaymentType(payment["type"])

    @staticmethod
    def _validate_services(services):
        """Validate the data provided for each service if any were given"""
        for service in services:
            if set(service.keys()) != set(["id", "quantity"]):
                raise OrderCreate.InvalidService(service)

    @staticmethod
    def _validate_selected_offers(selected_offers):
        """Validate number of selected_offers"""
        if len(selected_offers) != 1:
            raise OrderCreate.InvalidSelectedOffersLength(len(selected_offers))

    @staticmethod
    def _validate_passengers(passengers):
        """Validate passenger count and the data provided for each if any were given"""
        if len(passengers) == 0:
            raise OrderCreate.InvalidNumberOfPassengers(passengers)
        for passenger in passengers:
            if not (
                "born_on" in passenger
                or "email" in passenger
                or "family_name" in passenger
                or "gender" in passenger
                or "given_name" in passenger
                or "id" in passenger
                or "phone_number" in passenger
                or "title" in passenger
            ):
                raise OrderCreate.InvalidPassenger(passenger)

    def _instant_order(self):
        """Determine whether this order's type is instant"""
        return self._payment_type is not None and self._payment_type != "hold"

    def _build_order_payload(self):
        """Build order payload"""
        data = {
            "type": self._payment_type,
            "passengers": self._passengers,
            "services": self._services,
            "selected_offers": self._selected_offers,
        }

        if self._instant_order():
            data["payments"] = self._payments
        else:
            data["type"] = self._payment_type

        return data

    def hold(self):
        """Set payment type to 'hold'. If this isn't called the type is 'instant'"""
        self._payment_type = "hold"
        return self

    def selected_offers(self, selected_offers):
        """Set selected_offers"""
        OrderCreate._validate_selected_offers(selected_offers)
        self._selected_offers = selected_offers
        return self

    def services(self, services):
        """Set services"""
        # TODO(nlopes): this should be its own type to ensure the user *only* passes valid
        # data
        OrderCreate._validate_services(services)
        self._services = services
        return self

    def payments(self, payments):
        """Set payment method"""
        # TODO(nlopes): this should be its own type to ensure the user *only* passes valid
        # data
        OrderCreate._validate_payments(payments)
        self._payments = payments
        return self

    def passengers(self, passengers):
        """Set passenger information for all passengers that will be travelling"""
        # TODO(nlopes): this should be its own type to ensure the user *only* passes valid
        # data
        OrderCreate._validate_passengers(passengers)
        self._passengers = passengers
        return self

    def execute(self):
        """POST /air/orders - trigger the call to create the order"""
        OrderCreate._validate_passengers(self._passengers)
        if self._instant_order():
            OrderCreate._validate_payments(self._payments)
        OrderCreate._validate_services(self._services)
        OrderCreate._validate_selected_offers(self._selected_offers)
        res = self._client.do_post(
            self._client._url,
            body={"data": self._build_order_payload()},
        )
        return Order.from_json(res["data"])


class OrderUpdate:
    """Auxiliary class to provide methods for order update related data"""

    class InvalidMetadata(Exception):
        """Invalid metadata data provided"""

    def __init__(self, client, id_):
        self._client = client
        self._id = id_
        self._metadata = {}

    @staticmethod
    def _validate_metadata(metadata):
        """Validate structure of Metadata"""
        if type(metadata) is not dict:
            raise OrderUpdate.InvalidMetadata(metadata)

    def metadata(self, metadata):
        """Set the Order Metadata."""
        self._metadata = metadata
        OrderUpdate._validate_metadata(self._metadata)
        return self

    def execute(self):
        """PATCH /air/orders/{:id} - trigger the call to update the order."""
        OrderUpdate._validate_metadata(self._metadata)

        url = f"{self._client._url}/{self._id}"

        res = self._client.do_patch(
            url,
            body={"data": {"metadata": self._metadata}},
        )
        if res is not None:
            return Order.from_json(res["data"])
