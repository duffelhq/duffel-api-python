from ..http_client import HttpClient, Pagination
from ..models import OfferRequest


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
        return OfferRequest(self.do_get("{}/{}".format(self._url, id_))["data"])

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

    def __init__(self, client):
        self._client = client
        self._return_offers = "false"
        self._cabin_class = "economy"
        self._passengers = []
        self._slices = []

    def _validate_cabin_class(cabin_class):
        """Validate cabin class"""
        if cabin_class not in [
            "first",
            "business",
            "economy",
            "premium_economy",
        ]:
            raise OfferRequestCreate.InvalidCabinClass(cabin_class)

    def _validate_passengers(passengers):
        """Validate passenger count and the data provided for each if any were given"""
        if len(passengers) == 0:
            raise OfferRequestCreate.InvalidNumberOfPassengers(passengers)
        for passenger in passengers:
            if not ("type" in passenger or "age" in passenger):
                raise OfferRequestCreate.InvalidPassenger(passenger)

    def _validate_slices(slices):
        """Validate number of slices and the data provided for each if any were given"""
        if len(slices) == 0:
            raise OfferRequestCreate.InvalidNumberOfSlices(slices)
        for travel_slice in slices:
            if set(travel_slice.keys()) != set(
                ["departure_date", "destination", "origin"]
            ):
                raise OfferRequestCreate.InvalidSlice(travel_slice)

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
                    "slices": self._slices,
                }
            },
        )
        return OfferRequest(res["data"])
