from duffel_api.models import LoyaltyProgrammeAccount


def test_loyalty_programme_account_model_parsing():
    json = {"airline_iata_code": "BA", "account_number": "12901014"}
    assert LoyaltyProgrammeAccount.from_json(json)
