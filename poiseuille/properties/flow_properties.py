from ..units.units import Unit

class FlowProperty:
    def __init__(self, value=0, min=None, max=None):
        self.value = value
        self.min = min
        self.max = max

    def name(self):
        return 'Flow property'

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value + other.value

class FlowRate(FlowProperty):
    UNITS = Unit(L=3, T=-1)

    def __init__(self, value=0):
        super().__init__(value=value)

    def name(self):
        return 'Flow rate'

class Pressure(FlowProperty):
    def __init__(self, value=0):
        super().__init__(value=value)

    def name(self):
        return 'Pressure'

