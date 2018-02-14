from math import pi, sqrt

from poiseuille.components.base.connectors import Connector


class ProcterAndGambleConnector(Connector):
    TYPE = 'Procter and Gamble Connector'
    UNITS = {
        'Length': 'ft',
        'Diameter': 'in',
        'Flow rate': 'CFM',
        'Velocity pressure': 'in H2O'
    }

    def __init__(self, length=50., diameter=6., k_ent=0.):
        super().__init__(name='Line')
        self.length = length
        self.diameter = diameter
        self.k_ent = k_ent
        self.r = 1e-10
        self.flow_rate = 0.
        self.velocity_pressure = 0.
        self.update_properties()

    def properties(self):
        return {
            'Length': self.length,
            'Diameter': self.diameter,
            'Entrance coeff': self.k_ent
        }

    def property_ranges(self):
        return {
            'Length': (0, None),
            'Diameter': (0, None),
            'Entrance coeff': (0, None)
        }

    def solution(self):
        return {
            'Resistance': self.r,
            'Flow rate': self.flow_rate,
            'Velocity pressure': self.velocity_pressure
        }

    def update_properties(self, **kwargs):
        self.length = kwargs.get('Length', self.length)
        self.diameter = kwargs.get('Diameter', self.diameter)
        self.k_ent = kwargs.get('Entrance coeff', self.k_ent)

        # Computed properties
        self.area = pi * (self.diameter / 24.) ** 2
        self.coeff = 2.238 / self.diameter * (1. / 1000.) ** 2 * (
                    0.1833 + (1. / self.diameter) ** (1. / 3.)) * self.length / (100. * self.area ** 2)
        self.coeff += self.k_ent / (4005 ** 2 * self.area ** 2)

    def update_solution(self):
        self.r = sqrt(self.coeff * abs(self.input.p - self.output.p)) + 1e-10
        self.flow_rate = (self.input.p - self.output.p) / self.r
        self.velocity_pressure = (self.flow_rate / self.area / 4005) ** 2
