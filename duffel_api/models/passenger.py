from ..models import LoyaltyProgrammeAccount


class Passenger:
    """The passenger travelling"""

    allowed_types = ["adult"]

    class InvalidType(Exception):
        """Invalid passenger type provided"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "type" and value and value not in Passenger.allowed_types:
                raise Passenger.InvalidType(value)
            if key == "loyalty_programme_accounts":
                value = [
                    LoyaltyProgrammeAccount(loyalty_programme_account)
                    for loyalty_programme_account in value
                ]

            setattr(self, key, value)
