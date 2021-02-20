class Aircraft:
    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])
