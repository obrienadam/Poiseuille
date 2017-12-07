from math import pi, sqrt


class Resistance:
    def __init__(self, r=1.):
        self.r = r
        self.flow_rate = 0.

    def update_solution(self, input, output):
        self.flow_rate = (input.p - output.p) / self.r


class ProctorAndGambleResistance(Resistance):
    def __init__(self, l=50., d=6., k_ent=0.):
        super().__init__(r=1.)
        self.l = l
        self.d = d
        self.k_ent = k_ent
        self.update_properties()

    def update_properties(self, **properties):
        self.l = properties.get('Length', self.l)
        self.d = properties.get('Diameter', self.d)
        self.k_ent = properties.get('Entrance coefficient', self.k_ent)
        area = pi * (self.d / 24.) ** 2
        self.coeff = 2.238 / self.d * (1. / 1000.) ** 2 * (0.1833 + (1. / self.d) ** (1. / 3.)) * self.l / (
                100. * area ** 2)
        self.coeff += self.k_ent / (4005 ** 2 * area ** 2)

    def update_solution(self, input, output):
        self.r = sqrt(self.coeff * abs(input.p - output.p)) + 1e-10
        super().update_solution(input, output)
