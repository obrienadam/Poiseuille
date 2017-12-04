from math import pi, sqrt


class Connector(object):
    def __init__(self, **properties):
        for key, value in properties.items():
            setattr(self, key, value)

        self.input = None
        self.output = None

    def connect(self, input, output):
        if input.can_connect(output):
            self.input = input
            self.output = output
            input.connector = self
            output.connector = self
            return True

        return False

    def other(self, node):
        if node is self.input:
            return self.output
        elif node is self.output:
            return self.input
        else:
            raise ValueError('Node is not attached to this connector.')

    def update_properties(self):
        raise NotImplementedError

    def update_solution(self):
        raise NotImplementedError


class PoiseuilleConnector(Connector):
    def __init__(self, r=1., **proerties):
        super(PoiseuilleConnector, self).__init__(r=r, flow_rate=0., **proerties)

    def update_solution(self):
        self.flow_rate = (self.input.p - self.output.p) / self.r

class LinearConnector(Connector):
    def __init__(self, r=1., **properties):
        super().__init__(r=r, flow_rate=0., **properties)

    def update_solution(self):
        self.flow_rate = (self.input.p - self.output.p) / self.r

class ProctorAndGambleConnector(PoiseuilleConnector):
    def __init__(self, l=50., d=6., k_ent=0.):
        super(ProctorAndGambleConnector, self).__init__(r=1., l=l, d=d, k_ent=k_ent)
        area = pi * (self.d / 24.) ** 2
        self.coeff = 2.238 / self.d * (1. / 1000.) ** 2 * (0.1833 + (1. / self.d) ** (1. / 3.)) * self.l / (
                100. * area ** 2)
        self.coeff += self.k_ent / (4005 ** 2 * area ** 2)

    def update_solution(self):
        self.r = sqrt(self.coeff * abs(self.input.p - self.output.p)) + 0.0001
        self.flow_rate = (self.input.p - self.output.p) / self.r
