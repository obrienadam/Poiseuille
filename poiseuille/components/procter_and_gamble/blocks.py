from poiseuille.components.base.blocks import Block
from poiseuille.components.base.nodes import Node, Input, Output
from poiseuille.equation.equation import Equation, Term

class PressureReservoir(Block):
    def __init__(self, p=0.):
        super(PressureReservoir, self).__init__(name='PATM')
        self.p = p
        self.node = Node(self, p=0.)
        self.add_nodes(self.node)

    def type(self):
        return 'Pressure Reservoir'

    def properties(self):
        return {'Pressure': self.p}

    def solution(self):
        return {}

    def equations(self):
        return [Equation([Term(self.node, 1.)], self.p)]

    def update_properties(self, **kwargs):
        self.p = kwargs.get('Pressure', self.p)

    def update_solution(self):
        pass


class Fan(Block):
    def __init__(self, dp=0.):
        super(Fan, self).__init__(name='Fan')
        self.dp = dp
        self.power = 0.
        self.flow_rate = 0.
        self.input = Input(self, p=0.)
        self.output = Output(self, p=0.)
        self.add_nodes(self.input, self.output)

    def type(self):
        return 'Fan'

    def properties(self):
        return {'Pressure differential': self.dp}

    def solution(self):
        return {'Flow rate': self.flow_rate, 'Power': self.power}

    def equations(self):
        return [Equation([Term(self.input, -1.), Term(self.output, 1.)], self.dp), self.continuity_equation()]

    def update_properties(self, **kwargs):
        self.dp = kwargs.get('Pressure differential', self.dp)

    def update_solution(self):
        pass


class ConstantDeliveryFan(Block):
    def __init__(self, flow_rate=0.):
        super(ConstantDeliveryFan, self).__init__()
        self.flow_rate = flow_rate
        self.dp = 0.
        self.input = Input(self, p=0.)
        self.output = Output(self, p=0.)
        self.add_nodes(self.input, self.output)

    def type(self):
        return 'Constant Delivery Fan'

    def properties(self):
        return {'Flow rate': self.flow_rate}

    def solution(self):
        return {'Pressure differential': self.dp}

    def equations(self):
        r = self.input.connector.r + self.output.connector.r
        eqn = Equation([Term(self.input, -1. / r), Term(self.output, 1. / r)], self.flow_rate)
        return [eqn, self.continuity_equation()]

    def update_properties(self, **kwargs):
        self.flow_rate = kwargs.get('Flow rate', self.flow_rate)

    def update_solution(self):
        self.dp = self.output.p - self.input.p


class PowerCurveFan(Fan):
    def __init__(self, fcn):
        self.fcn = fcn
        self.flow_rate = 0.
        super(PowerCurveFan, self).__init__(dp=self.fcn(self.flow_rate))

    def type(self):
        return 'Power Curve Fan'

    def update_properties(self):
        self.flow_rate = self.input.connector.flow_rate
        self.dp = self.fcn(self.flow_rate)


class ResistorValve(Block):
    def __init__(self, r=0., min_r=1e-12):
        super().__init__(name='R')
        self.r = r
        self.min_r = min_r
        self.input, self.output = Node(self, p=0.), Node(self, p=0.)
        self.add_nodes(self.input, self.output)
        self.flow_rate = 0.

    def type(self):
        return 'Resistor Valve'

    def properties(self):
        return {'Resistance': self.r}

    def solution(self):
        return {}

    def equations(self):
        p1 = self.input.connector.other(self.input)
        p2 = self.input
        p3 = self.output
        r1 = self.input.connector.r
        rv = self.r
        eqn = Equation([Term(p2, rv / r1 + 1), Term(p1, -rv / r1), Term(p3, -1)])
        return [eqn, self.continuity_equation()]

    def update_properties(self, **kwargs):
        self.r = kwargs.get('Resistance', self.r)
        self.min_r = kwargs.get('Minimum resistance', self.min_r)

    def update_solution(self):
        if self.r != 0.:
            self.flow_rate = (self.input.p - self.output.p) / self.r
        else:
            self.flow_rate = self.input.connector.flow_rate


class RestrictorValve(ResistorValve):
    def __init__(self, max_flow_rate=0., allow_backflow=True):
        super().__init__(r=0)
        self.max_flow_rate = max_flow_rate
        self.allow_backflow = allow_backflow

    def type(self):
        return 'Restrictor Valve'

    def properties(self):
        return {
            'Max flow rate': self.max_flow_rate,
        }

    def solution(self):
        return {
            'Flow rate': self.flow_rate,
            'Resistance': self.r,
        }

    def equations(self):
        if abs(self.flow_rate) > abs(self.max_flow_rate):
            r_line = self.input.connector.r + self.output.connector.r
            dp_line = abs(self.input.connector.other(self.input).p - self.output.connector.other(self.output).p)
            self.r = dp_line / self.max_flow_rate - r_line
        else:
            self.r = 0.

        return super().equations()

    def update_properties(self, **kwargs):
        self.max_flow_rate = kwargs.get('Max flow rate', self.max_flow_rate)


class PerfectSplitter(Block):
    def __init__(self, num_outputs=1):
        super(PerfectSplitter, self).__init__()
        self.input = Input(self, p=0)
        self.outputs = [Output(self, p=0) for i in range(num_outputs)]
        self.add_nodes(self.input, *self.outputs)

    def type(self):
        return 'Perfect Splitter'

    def equations(self):
        eqns = [Equation([Term(self.input, 1), Term(output, -1)], 0.) for output in self.outputs]
        eqns.append(self.continuity_equation())

        return eqns

    def update_solution(self):
        pass


class PerfectJunction(Block):
    def __init__(self, num_nodes=1):
        super(PerfectJunction, self).__init__()
        self.nodes = [Node(self, p=0) for i in range(num_nodes)]

    def type(self):
        return 'Perfect Junction'

    def equations(self):
        eqns = [Equation([Term(self.nodes[-1], 1.), Term(node, -1.)], 0.) for node in self.nodes[:-1]]
        eqns.append(self.continuity_equation())

        return eqns

    def update_solution(self):
        pass
