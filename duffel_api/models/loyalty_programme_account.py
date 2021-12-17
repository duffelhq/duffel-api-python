class LoyaltyProgrammeAccount:
    """A passenger's loyalty programme account"""

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])
