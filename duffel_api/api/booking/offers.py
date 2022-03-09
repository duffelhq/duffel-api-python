from ...http_client import HttpClient, Pagination
from ...models import Offer, OfferPassenger


class OfferClient(HttpClient):
    """Client to interact with Offers"""

    def __init__(self, **kwargs):
        self._url = "/air/offers"
        super().__init__(**kwargs)

    class InvalidOfferId(Exception):
        """Invalid offer ID data provided"""

    class InvalidOfferPassengerId(Exception):
        """Invalid offer passenger ID data provided"""

    class InvalidFamilyName(Exception):
        """Invalid family name data provided"""

    class InvalidGivenName(Exception):
        """Invalid given name data provided"""

    class MissingLoyaltyProgrammeAccountValue(Exception):
        """A value was was missing in the data provided"""

    class InvalidLoyaltyProgrammeAirlineIataCode(Exception):
        """Invalid loyalty programme account airline IATA code data provided"""

    class InvalidLoyaltyProgrammeAccountNumber(Exception):
        """Invalid loyalty programme account account number data provided"""

    @staticmethod
    def _validate_update_passenger_args(
        offer_id,
        offer_passenger_id,
        family_name,
        given_name,
        loyalty_programme_accounts,
    ):
        """Validates passenger details"""

        if not offer_id.strip():
            raise OfferClient.InvalidOfferId(offer_id)
        if not offer_passenger_id.strip():
            raise OfferClient.InvalidOfferPassengerId(offer_passenger_id)
        if not family_name.strip():
            raise OfferClient.InvalidFamilyName(family_name)
        if not given_name.strip():
            raise OfferClient.InvalidGivenName(given_name)
        for loyalty_programme_account in loyalty_programme_accounts:
            if "airline_iata_code" not in loyalty_programme_account:
                raise OfferClient.MissingLoyaltyProgrammeAccountValue(
                    "airline_iata_code"
                )
            if "account_number" not in loyalty_programme_account:
                raise OfferClient.MissingLoyaltyProgrammeAccountValue("account_number")
            if not loyalty_programme_account["airline_iata_code"].strip():
                raise OfferClient.InvalidLoyaltyProgrammeAirlineIataCode(
                    loyalty_programme_account["airline_iata_code"]
                )
            if not loyalty_programme_account["account_number"].strip():
                raise OfferClient.InvalidLoyaltyProgrammeAccountNumber(
                    loyalty_programme_account["account_number"]
                )

    def get(self, id_, return_available_services=False):
        """GET /air/offers/:id"""
        params = {}
        if return_available_services:
            params["return_available_services"] = "true"

        response = self.do_get(f"{self._url}/{id_}", query_params=params)
        if response is not None:
            return Offer.from_json(response["data"])

    def list(self, offer_request_id, sort=None, max_connections=None, limit=50):
        """GET /air/offers"""
        params = {"limit": limit, "offer_request_id": offer_request_id}
        if sort:
            params["sort"] = sort
        if max_connections:
            params["max_connections"] = max_connections
        return Pagination(self, Offer, params)

    def update_passenger(
        self,
        offer_id,
        offer_passenger_id,
        family_name,
        given_name,
        loyalty_programme_accounts,
    ):
        """PATCH /air/offers/:offer_id/passengers/:passenger_id"""

        OfferClient._validate_update_passenger_args(
            offer_id,
            offer_passenger_id,
            family_name,
            given_name,
            loyalty_programme_accounts,
        )

        url = f"{self._url}/{offer_id}/passengers/{offer_passenger_id}"
        body = {
            "data": {
                "loyalty_programme_accounts": [
                    {
                        "airline_iata_code": loyalty_programme_account[
                            "airline_iata_code"
                        ],
                        "account_number": loyalty_programme_account["account_number"],
                    }
                    for loyalty_programme_account in loyalty_programme_accounts
                ],
                "given_name": given_name,
                "family_name": family_name,
            }
        }

        res = self.do_patch(url, body=body)
        if res is not None:
            return OfferPassenger.from_json(res["data"])
