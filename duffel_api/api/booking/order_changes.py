from ...http_client import HttpClient
from ...models import OrderChange


class OrderChangeClient(HttpClient):
    """Entrypoint to create and confirm order changes."""

    class InvalidPayment(Exception):
        """Invalid payment data provided"""

    class InvalidPaymentType(Exception):
        """Invalid payment type provided"""

    @staticmethod
    def _validate_payment(payment):
        """Validate payment for the order change."""
        if set(payment.keys()) != set(["amount", "currency", "type"]):
            raise OrderChangeClient.InvalidPayment(payment)
        if payment["type"] not in ["arc_bsp_cash", "balance", "payments"]:
            raise OrderChangeClient.InvalidPaymentType(payment["type"])

    def __init__(self, **kwargs):
        """Instantiate an order change client."""
        self._url = "/air/order_changes"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/order_changes/:id."""
        res = self.do_get(f"{self._url}/{id_}")
        if res is not None:
            return OrderChange.from_json(res["data"])

    def create(self, selected_order_change_offer):
        """Create a pending order change.

        To begin the process of changing an order you need to create an order
        change. The OrderChange will contain the `selected_order_change_offer`
        reference of the change you wish to make to your order.

        To proceed, you must confirm the change using the Confirm an order
        change endpoint.
        """
        res = self.do_post(
            self._url,
            body={"data": {"selected_order_change_offer": selected_order_change_offer}},
        )
        if res is not None:
            return OrderChange.from_json(res["data"])

    def confirm(self, id_, payment_):
        """Confirm an order change.

        Once you've created a pending order change, you'll know the
        `change_total_amount` due for the change.

        To actually change the order, you'll need to confirm the change. The
        booking with the airline will be updated with the new slice you
        previously chose, and the change_total_amount will be charged to your
        specific payment type.

        If the amount of change_total_amount is negative, then this will be
        returned to the refund_to method (e.g. your Duffel balance). You'll
        then need to refund your customer (e.g. back to their credit/debit
        card).
        """
        OrderChangeClient._validate_payment(payment_)

        url = f"{self._url}/{id_}/actions/confirm"

        res = self.do_post(
            url,
            body={
                "data": {
                    "payment": {
                        "amount": payment_["amount"],
                        "currency": payment_["currency"],
                        "type": payment_["type"],
                    }
                }
            },
        )
        if res is not None:
            return OrderChange.from_json(res["data"])
