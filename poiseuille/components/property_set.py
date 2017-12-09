class Properties:
    def __init__(self, properties={}, units={}):
        self.properties = properties
        self.units = units

    def get_units(self, property):
        return self.units.get(property, 'N/A')

class SIProperties(Properties):
    def __init__(self):
        properties = {
            'Length': 'm',
            'Mass': 'kg',
            'Flow rate': 'm^3/s'
        }

class ProcterAndGambleProperties(Properties):
    def __init__(self):
        pass
