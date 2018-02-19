from math import copysign

from poiseuille.components.base.blocks import Block
from poiseuille.components.base.nodes import Node, Input, Output
from poiseuille.equation.equation import Equation, Term


class ProcterAndGambleBlock(Block):
    UNITS = {
        'Pressure': 'in H2O',
        'Pressure differential': 'in H2O',
        'Flow rate': 'CFM',
        'Max flow rate': 'CFM',
        'Resistance': 'in H2O/CFM'
    }

    SYMBOLS = {
        'Pressure': 'p',
        'Pressure differential': 'dp',
        'Flow rate': 'flow_rate',
        'Max flow rate': 'max_flow_rate',
        'Resistance': 'r'
    }

    def __init__(self, name='P&G Block'):
        super().__init__(name=name)


class PressureReservoir(ProcterAndGambleBlock):
    TYPE = 'Pressure Reservoir'

    def __init__(self, p=0.):
        super().__init__(name='PATM')
        self.p = p
        self.node = Node(self, p=0.)
        self.add_nodes(self.node)

    def properties(self):
        return {
            'Pressure': {'value': self.p, 'range': (float('-inf'), float('inf'))}
        }

    def solution(self):
        return {}

    def equations(self):
        return [Equation([Term(self.node, 1.)], self.p)]

    def update_properties(self, **kwargs):
        self.p = kwargs.get('Pressure', self.p)

    def update_solution(self):
        pass


class Fan(ProcterAndGambleBlock):
    TYPE = 'Fan'

    def __init__(self, dp=0., name='Fan'):
        super().__init__(name=name)
        self.dp = dp
        self.power = 0.
        self.flow_rate = 0.
        self.input = Input(self, p=0.)
        self.output = Output(self, p=0.)
        self.add_nodes(self.input, self.output)

    def type(self):
        return 'Fan'

    def properties(self):
        return {
            'Pressure differential': {'value': self.dp, 'range': (0., float('inf'))}
        }

    def solution(self):
        return {'Flow rate': self.flow_rate}

    def equations(self):
        return [Equation([Term(self.input, -1.), Term(self.output, 1.)], self.dp), self.continuity_equation()]

    def update_properties(self, **kwargs):
        self.dp = kwargs.get('Pressure differential', self.dp)

    def update_solution(self):
        self.flow_rate = self.input.connector.flow_rate


class ConstantDeliveryFan(ProcterAndGambleBlock):
    TYPE = 'Constant Delivery Fan'

    def __init__(self, flow_rate=0.):
        super().__init__(name='Q Fan')
        self.flow_rate = flow_rate
        self.dp = 0.
        self.input = Input(self, p=0.)
        self.output = Output(self, p=0.)
        self.add_nodes(self.input, self.output)

    def properties(self):
        return {
            'Flow rate': {'value': self.flow_rate, 'range': (0., float('inf'))}
        }

    def solution(self):
        return {'Pressure differential': self.dp}

    def equations(self):
        r = self.input.connector.r
        eqn = Equation([Term(self.input.connector.other(self.input), 1. / r), Term(self.input, -1. / r)],
                       rhs=self.flow_rate)
        return [eqn, self.continuity_equation()]

    def update_properties(self, **kwargs):
        self.flow_rate = kwargs.get('Flow rate', self.flow_rate)

    def update_solution(self):
        self.dp = self.output.p - self.input.p


class PowerCurveFan(Fan):
    TYPE = 'Power Curve Fan'

    def __init__(self, fcn):
        super().__init__(dp=0., name='Fan (PC)')
        self.fcn = fcn

    def properties(self):
        return {}

    def solution(self):
        return {
            'Pressure differential': self.dp,
            'Power': self.power,
        }

    def update_properties(self):
        pass

    def update_solution(self):
        self.flow_rate = (self.input.connector.other(self.input).p - self.input.p) / self.input.connector.r
        self.dp = self.fcn(self.flow_rate)
        self.power = self.flow_rate * self.dp


class ResistorValve(ProcterAndGambleBlock):
    TYPE = 'Resistor Valve'

    def __init__(self, r=0., min_r=1e-12):
        super().__init__(name='R')
        self.r = r
        self.min_r = min_r
        self.input, self.output = Node(self, p=0.), Node(self, p=0.)
        self.add_nodes(self.input, self.output)
        self.flow_rate = 0.

        self.constraints = {
            'Flow rate': {
                'type': 'eq',
                'value': 0.,
                'active': False,
                'dependent': True,
                'optional': True
            }
        }

    def properties(self):
        return {
            'Resistance': {'value': self.r, 'range': (0., float('inf'))}
        }

    def solution(self):
        return {'Flow rate': self.flow_rate}

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
        self.flow_rate = copysign(self.input.connector.flow_rate, self.input.p - self.output.p)


class PerfectSplitter(ProcterAndGambleBlock):
    TYPE = 'Perfect Splitter'

    def __init__(self, num_outputs=1):
        super().__init__(name='Splitter')
        self.input = Input(self, p=0)
        self.outputs = [Output(self, p=0) for i in range(num_outputs)]
        self.add_nodes(self.input, *self.outputs)

    def equations(self):
        r1 = self.outputs[0].connector.area / self.input.connector.area
        r2 = self.outputs[1].connector.area / self.input.connector.area

        eqns = [
            Equation([Term(self.outputs[0], 1.), Term(self.input, -r1)]),
            Equation([Term(self.outputs[1], 1.), Term(self.input, -r2)])
        ]

        eqns.append(self.continuity_equation())

        return eqns

    def update_solution(self):
        pass


class PerfectJunction(ProcterAndGambleBlock):
    TYPE = 'Perfect Junction'

    def __init__(self, num_nodes=1):
        super().__init__(name='Junction')
        self.nodes = [Node(self, p=0) for i in range(num_nodes)]

    def equations(self):
        eqns = []
        for node in self.nodes[:-1]:
            ratio = node.connector.area / self.nodes[-1].connector.area
            eqns.append(
                Equation([Term(node, 1.), Term(self.nodes[-1], -ratio)])
            )

        eqns = [Equation([Term(self.nodes[-1], 1.), Term(node, -1.)], 0.) for node in self.nodes[:-1]]
        eqns.append(self.continuity_equation())

        return eqns

    def update_solution(self):
        pass


class Joiner(ProcterAndGambleBlock):
    TYPE = 'Joiner'

    def __init__(self, k_regain=0.6, k_loss=1):
        super().__init__(name='Joiner')
        self.k_regain = k_regain
        self.k_loss = k_loss
        self.input_1 = Input(self, p=0)
        self.input_2 = Input(self, p=0)
        self.output = Output(self, p=0)
        self.add_nodes(self.input_1, self.input_2, self.output)

    def properties(self):
        return {
            'Regain coefficient': {'value': self.k_regain, 'range': (0., 1.)},
            'Loss coefficient': {'value': self.k_loss, 'range': (0., float('inf'))}
        }

    def solution(self):
        if all([node.connector for node in self.nodes]):
            vp_1 = self.input_1.connector.velocity_pressure
            vp_2 = self.input_2.connector.velocity_pressure
            vp_3 = self.output.connector.velocity_pressure
        else:
            vp_1 = vp_2 = vp_3 = 0.

        return {
            'Line 1 regain': vp_1 - vp_3 > 0,
            'Line 2 regain': vp_2 - vp_3 > 0
        }

    def equations(self):
        c1 = self.input_1.connector
        c2 = self.input_2.connector
        c3 = self.output.connector
        vp_1 = c1.velocity_pressure
        vp_2 = c2.velocity_pressure
        vp_3 = c3.velocity_pressure
        q1 = c1.flow_rate
        q2 = c2.flow_rate
        q3 = c3.flow_rate

        if vp_1 - vp_3 > 0:
            a1 = self.k_regain * vp_1 / q1 if q1 != 0. else 0.
            a3 = -self.k_regain * vp_3 / q3 if q3 != 0. else 0.
        else:
            a1 = self.k_loss * vp_1 / q1 if q1 != 0. else 0.
            a3 = -self.k_loss * vp_3 / q3 if q3 != 0. else 0.

        eqn1 = Equation([
            Term(self.output, 1),
            Term(self.input_1, -1),
            Term(c1.input, a1 / c1.r),
            Term(c1.output, -a1 / c1.r),
            Term(c3.input, -a3 / c3.r),
            Term(c3.output, a3 / c3.r)
        ])

        if vp_2 - vp_3 > 0:
            a2 = self.k_regain * vp_2 / q2 if q2 != 0. else 0.
            a3 = -self.k_regain * vp_3 / q3 if q3 != 0. else 0.
        else:
            a2 = self.k_loss * vp_2 / q2 if q2 != 0. else 0.
            a3 = -self.k_loss * vp_3 / q3 if q3 != 0. else 0.

        eqn2 = Equation([
            Term(self.output, 1),
            Term(self.input_2, -1),
            Term(c1.input, a2 / c2.r),
            Term(c1.output, -a2 / c2.r),
            Term(c3.input, -a3 / c3.r),
            Term(c3.output, a3 / c3.r)
        ])

        return [self.continuity_equation(), eqn1, eqn2]

    def update_properties(self, **kwargs):
        self.k_regain = kwargs.get('Regain coefficient', self.k_regain)
        self.k_loss = kwargs.get('Loss coefficient', self.k_loss)

    def update_solution(self, **kwargs):
        pass
