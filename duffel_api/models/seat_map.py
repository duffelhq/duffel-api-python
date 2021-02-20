class SeatMap:
    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'cabins':
                value = [SeatMapCabin(v) for v in value]
            setattr(self, key, value)


class SeatMapCabin:
    allowed_classes = ['first', 'business', 'premium_economy', 'economy']

    class InvalidClass(Exception):
        pass

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'cabin_class' and value not in SeatMapCabin.allowed_classes:
                raise SeatMapCabin.InvalidClass(value)
            elif key == 'wings' and value:
                value = SeatMapCabinWings(value)
            elif key == 'rows':
                value = [SeatMapCabinRow(r) for r in value]
            setattr(self, key, value)


class SeatMapCabinRow:
    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'sections':
                value = [SeatMapCabinRowSection(s) for s in value]
            setattr(self, key, value)


class SeatMapCabinRowSection:
    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == 'elements':
                value = [SeatMapCabinRowSectionElement(s) for s in value]
            setattr(self, key, value)


class SeatMapCabinRowSectionElement:
    allowed_types = ['seat', 'bassinet', 'empty', 'exit_row', 'lavatory', 'galley',
                     'closet', 'stairs']

    class InvalidType(Exception):
        pass

    def __init__(self, json):
        element_type = json['type']
        if element_type not in SeatMapCabinRowSectionElement.allowed_types:
            raise SeatMapCabinRowSectionElement.InvalidType(element_type)

        if element_type == 'seat':
            for key in json:
                value = json[key]
                if key == 'available_services':
                    value = [SeatMapCabinRowSectionElementSeatService(s) for s in value]
                setattr(self, key, value)
        else:
            setattr(self, 'type', element_type)


class SeatMapCabinRowSectionElementSeatService:
    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])


class SeatMapCabinWings:
    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])
