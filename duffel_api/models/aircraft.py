class Aircraft:
    """Aircraft are used to describe what passengers will fly in for a given trip"""

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])
