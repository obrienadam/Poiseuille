from math import pi, sqrt
from .resistance_functions import Resistance


class Connector(object):
    def __init__(self, r_func=Resistance(), name='C', **properties):
        self.name = name
        self.r_func = r_func

        for key, value in properties.items():
            setattr(self, key, value)

        self.input = None
        self.output = None

    def connect(self, input, output):
        if input.can_connect(output):
            self.disconnect()
            self.input = input
            self.output = output
            input.connector = self
            output.connector = self
            return True

        return False

    def disconnect(self):
        if self.input:
            self.input.connector = None

        if self.output:
            self.output.connector = None

        self.input = None
        self.output = None

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
        self.r_func.update_solution(self.input, self.output)

    @property
    def r(self):
        return self.r_func.r

    @property
    def flow_rate(self):
        return self.r_func.flow_rate
