class Airline:
    """Airlines are used to identify the air travel companies selling and operating
    flights

    """

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])
