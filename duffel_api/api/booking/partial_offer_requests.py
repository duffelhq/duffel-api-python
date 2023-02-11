from ...http_client import HttpClient
from ...models import OfferRequest


class PartialOfferRequestClient(HttpClient):
    """To search for and select flights separately for each slice of the journey, you'll
    need to create a partial offer reques. A partial offer request describes the
    passengers and where and when they want to travel (in the form of a list of
    slices). It may also include additional filters (e.g. a particular cabin to
    travel in).

    """

    def __init__(self, **kwargs):
        self._url = "/air/partial_offer_requests"
        super().__init__(**kwargs)

    def get(self, id_, selected_partial_offer=None):
        """GET /air/partial_offer_requests/:id

        If a selected_partial_offer is passed:
        GET /air/partial_offer_requests/:id?selected_partial_offer[]=:selected_partial_offer


        Retrieves a partial offers request by its ID, only including partial offers for
        the current slice of multi-step search flow.
        """  # noqa: E501
        response = None
        if selected_partial_offer is None:
            response = self.do_get(f"{self._url}/{id_}")
        else:
            response = self.do_get(
                f"{self._url}/{id_}",
                query_params={"selected_partial_offer[]": selected_partial_offer},
            )

        if response is not None:
            return OfferRequest.from_json(response["data"])

    def fares(self, id_, selected_partial_offers=[]):
        """GET /air/partial_offer_requests/:id/fares

        Retrieves an offer request with offers for fares matching selected partial offers.
        """
        response = self.do_get(
            f"{self._url}/{id_}/fares",
            query_params={"selected_partial_offer[]": selected_partial_offers},
        )
        if response is not None:
            return OfferRequest.from_json(response["data"])

    def create(self):
        """Initiate creation of a Partial Offer Request"""
        return PartialOfferRequestCreate(self)


class PartialOfferRequestCreate(object):
    """Auxiliary class to provide methods for partial offer request creation related data"""  # noqa: E501

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
            raise PartialOfferRequestCreate.InvalidCabinClass(cabin_class)

    @staticmethod
    def _validate_passengers(passengers):
        """Validate passenger count and the data provided for each if any were given"""
        if len(passengers) == 0:
            raise PartialOfferRequestCreate.InvalidNumberOfPassengers(passengers)
        for passenger in passengers:
            if not ("type" in passenger or "age" in passenger):
                raise PartialOfferRequestCreate.InvalidPassenger(passenger)

    @staticmethod
    def _validate_slices(slices):
        """Validate number of slices and the data provided for each if any were given"""
        if len(slices) == 0:
            raise PartialOfferRequestCreate.InvalidNumberOfSlices(slices)
        for travel_slice in slices:
            if set(travel_slice.keys()) != set(
                ["departure_date", "destination", "origin"]
            ):
                raise PartialOfferRequestCreate.InvalidSlice(travel_slice)

    @staticmethod
    def _validate_max_connections(max_connections):
        """Validate the max connection number"""
        if not isinstance(max_connections, int) or max_connections < 0:
            raise PartialOfferRequestCreate.InvalidMaxConnectionValue(max_connections)

    def cabin_class(self, cabin_class):
        """Set cabin_class - defaults to 'economy'"""
        PartialOfferRequestCreate._validate_cabin_class(cabin_class)
        self._cabin_class = cabin_class
        return self

    def passengers(self, passengers):
        """Set the passengers that will be travelling"""
        PartialOfferRequestCreate._validate_passengers(passengers)
        self._passengers = passengers
        return self

    def slices(self, slices):
        """Set the slices for the origin-destination we want to travel"""
        PartialOfferRequestCreate._validate_slices(slices)
        self._slices = slices
        return self

    def max_connections(self, max_connections):
        """Set the max_connections for the journey we want to travel"""
        PartialOfferRequestCreate._validate_max_connections(max_connections)
        self._max_connections = max_connections
        return self

    def execute(self):
        """POST /air/partial_offer_requests - trigger the call to create the offer_request"""  # noqa: E501
        PartialOfferRequestCreate._validate_passengers(self._passengers)
        PartialOfferRequestCreate._validate_slices(self._slices)
        res = self._client.do_post(
            self._client._url,
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
