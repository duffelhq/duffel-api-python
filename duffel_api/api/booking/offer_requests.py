from ...http_client import HttpClient, Pagination
from ...models import OfferRequest


class OfferRequestClient(HttpClient):
    """To search for flights, you'll need to create an offer request.
    An offer request describes the passengers and where and when they want to
     travel (in the form of a list of slices). It may also include additional
    filters (e.g. a particular cabin to travel in).
    """

    def __init__(self, **kwargs):
        self._url = "/air/offer_requests"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/offer_requests/:id"""
        response = self.do_get(f"{self._url}/{id_}")

        if response is not None:
            return OfferRequest.from_json(response["data"])

    def list(self, limit=50):
        """GET /air/offer_requests"""
        return Pagination(self, OfferRequest, {"limit": limit})

    def create(self):
        """Initiate creation of an Offer Request"""
        return OfferRequestCreate(self)


class OfferRequestCreate(object):
    """Auxiliary class to provide methods for offer request creation related data"""

    class InvalidCabinClass(Exception):
        """Invalid cabin class provided"""

    class InvalidNumberOfPassengers(Exception):
        """Invalid number of passengers provided"""

    class InvalidNumberOfSlices(Exception):
        """Invalid number of slices provided"""

    class InvalidPassenger(Exception):
        """Invalid passenger data provided"""

    class InvalidSlice(Exception):
        """Invalid slice data provided"""

    class InvalidMaxConnectionValue(Exception):
        """Invalid max connection value provided"""

    def __init__(self, client):
        self._client = client
        self._return_offers = "false"
        self._cabin_class = "economy"
        self._passengers = []
        self._slices = []
        self._max_connections = 1

    @staticmethod
    def _validate_cabin_class(cabin_class):
        """Validate cabin class"""
        if cabin_class not in [
            "first",
            "business",
            "economy",
            "premium_economy",
        ]:
            raise OfferRequestCreate.InvalidCabinClass(cabin_class)

    @staticmethod
    def _validate_passengers(passengers):
        """Validate passenger count and the data provided for each if any were given"""
        if len(passengers) == 0:
            raise OfferRequestCreate.InvalidNumberOfPassengers(passengers)
        for passenger in passengers:
            if not ("type" in passenger or "age" in passenger):
                raise OfferRequestCreate.InvalidPassenger(passenger)

    @staticmethod
    def _validate_slices(slices):
        """Validate number of slices and the data provided for each if any were given"""
        if len(slices) == 0:
            raise OfferRequestCreate.InvalidNumberOfSlices(slices)
        for travel_slice in slices:
            if set(travel_slice.keys()) != set(
                ["departure_date", "destination", "origin"]
            ):
                raise OfferRequestCreate.InvalidSlice(travel_slice)

    @staticmethod
    def _validate_max_connections(max_connections):
        """Validate the max connection number"""
        if not isinstance(max_connections, int) or max_connections < 0:
            raise OfferRequestCreate.InvalidMaxConnectionValue(max_connections)

    def return_offers(self):
        """Set return_offers to 'true'"""
        self._return_offers = "true"
        return self

    def cabin_class(self, cabin_class):
        """Set cabin_class - defaults to 'economy'"""
        OfferRequestCreate._validate_cabin_class(cabin_class)
        self._cabin_class = cabin_class
        return self

    def passengers(self, passengers):
        """Set the passengers that will be travelling"""
        OfferRequestCreate._validate_passengers(passengers)
        self._passengers = passengers
        return self

    def slices(self, slices):
        """Set the slices for the origin-destination we want to travel"""
        OfferRequestCreate._validate_slices(slices)
        self._slices = slices
        return self

    def max_connections(self, max_connections):
        """Set the max_connections for the journey we want to travel"""
        OfferRequestCreate._validate_max_connections(max_connections)
        self._max_connections = max_connections
        return self

    def execute(self):
        """POST /air/offer_requests - trigger the call to create the offer_request"""
        OfferRequestCreate._validate_passengers(self._passengers)
        OfferRequestCreate._validate_slices(self._slices)
        res = self._client.do_post(
            self._client._url,
            query_params={"return_offers": self._return_offers},
            body={
                "data": {
                    "cabin_class": self._cabin_class,
                    "passengers": self._passengers,
                    "max_connections": self._max_connections,
                    "slices": self._slices,
                }
            },
        )
        return OfferRequest.from_json(res["data"])
