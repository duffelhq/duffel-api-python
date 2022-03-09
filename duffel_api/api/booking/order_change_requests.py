from ...http_client import HttpClient
from ...models import OrderChangeRequest


class OrderChangeRequestClient(HttpClient):
    """Client to interact with Order Change Requests"""

    def __init__(self, **kwargs):
        """Instantiate an order change request client."""
        self._url = "/air/order_change_requests"
        super().__init__(**kwargs)

    def create(self, order_id):
        """POST /air/order_change_requests"""
        return OrderChangeRequestCreate(self, order_id)

    def get(self, id_):
        """GET /air/order_change_requests/:id"""
        res = self.do_get(f"{self._url}/{id_}")
        if res is not None:
            return OrderChangeRequest.from_json(res["data"])


class OrderChangeRequestCreate:
    """Auxiliary class for order change request creation related data"""

    class InvalidOrderId(Exception):
        """Invalid order ID provided"""

    class InvalidSlices(Exception):
        """Invalid slices data provided"""

    def __init__(self, client, order_id):
        """Instantiate an order change request creation."""
        self._client = client
        self._order_id = order_id
        self._slices = []
        OrderChangeRequestCreate._validate_order_id(self._order_id)

    @staticmethod
    def _validate_order_id(order_id):
        """Set order ID"""
        if type(order_id) is not str:
            raise OrderChangeRequestCreate.InvalidOrderId(order_id)

    @staticmethod
    def _validate_slices(slices):
        """Validate structure of Metadata"""
        if type(slices) is not dict:
            raise OrderChangeRequestCreate.InvalidSlices(slices)

    def slices(self, slices):
        """Set slices"""
        self._slices = slices
        OrderChangeRequestCreate._validate_slices(self._slices)
        return self

    def execute(self):
        """POST /air/order_change_requests - trigger the call to create the
        order change request"""
        OrderChangeRequestCreate._validate_slices(self._slices)
        res = self._client.do_post(
            self._client._url,
            body={
                "data": {
                    "order_id": self._order_id,
                    "slices": self._slices,
                }
            },
        )
        return OrderChangeRequest.from_json(res["data"])
