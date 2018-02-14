from poiseuille.components.base.blocks import Block
from poiseuille.components.base.nodes import Node, Input, Output
from poiseuille.equation.equation import Equation, Term


class ProcterAndGambleBlock(Block):
    UNITS = {
        'Pressure': 'in H2O',
        'Pressure differential': 'in H2O',
        'Flow rate': 'CFM',
        'Max flow rate': 'CFM'
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
        return {'Pressure': self.p}

    def property_ranges(self):
        return {'Pressure': (-float('inf'), float('inf'))}

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

    def __init__(self, dp=0.):
        super().__init__(name='Fan')
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

    def property_ranges(self):
        return {'Pressure differential': (None, None)}

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
        return {'Flow rate': self.flow_rate}

    def property_ranges(self):
        return {'Flow rate': (None, None)}

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
        super().__init__(dp=self.fcn(self.flow_rate))
        self.fcn = fcn
        self.flow_rate = 0.

    def update_properties(self):
        self.flow_rate = self.input.connector.flow_rate
        self.dp = self.fcn(self.flow_rate)


class ResistorValve(ProcterAndGambleBlock):
    TYPE = 'Resistor Valve'

    def __init__(self, r=0., min_r=1e-12):
        super().__init__(name='R')
        self.r = r
        self.min_r = min_r
        self.input, self.output = Node(self, p=0.), Node(self, p=0.)
        self.add_nodes(self.input, self.output)
        self.flow_rate = 0.

    def properties(self):
        return {'Resistance': self.r}

    def property_ranges(self):
        return {'Resistance': (0, None)}

    def property_ranges(self):
        return {'Pressure differential': (None, None)}

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
    TYPE = 'Restrictor Valve'

    def __init__(self, max_flow_rate=0., allow_backflow=True):
        super().__init__(r=0)
        self.max_flow_rate = max_flow_rate
        self.allow_backflow = allow_backflow

    def properties(self):
        return {'Max flow rate': self.max_flow_rate}

    def property_ranges(self):
        return {'Max flow rate': (0, None)}

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


class PerfectSplitter(ProcterAndGambleBlock):
    TYPE = 'Perfect Splitter'

    def __init__(self, num_outputs=1):
        super().__init__(name='Splitter')
        self.input = Input(self, p=0)
        self.outputs = [Output(self, p=0) for i in range(num_outputs)]
        self.add_nodes(self.input, *self.outputs)

    def equations(self):
        eqns = [Equation([Term(self.input, 1), Term(output, -1)], 0.) for output in self.outputs]
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
            'Regain coefficient': self.k_regain,
            'Loss coefficient': self.k_loss
        }

    def property_ranges(self):
        return {
            'Regain coefficient': (0, 1),
            'Loss coefficient': (0, None)
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
        vp_1 = self.input_1.connector.velocity_pressure
        vp_2 = self.input_2.connector.velocity_pressure
        vp_3 = self.output.connector.velocity_pressure

        eqn1 = Equation([Term(self.output, 1), Term(self.input_1, -1)])
        eqn2 = Equation([Term(self.output, 1), Term(self.input_2, -1)])

        if vp_1 - vp_3 > 0:
            eqn1.rhs = self.k_regain * (vp_1 - vp_3)
        else:
            eqn1.rhs = self.k_loss * (vp_1 - vp_3)

        if vp_2 - vp_3 > 0:
            eqn2.rhs = self.k_regain * (vp_2 - vp_3)
        else:
            eqn2.rhs = self.k_loss * (vp_2 - vp_3)

        # eqn1 = Equation([Term(self.input_1, 1), Term(self.output, -1)])
        # eqn2 = Equation([Term(self.input_2, 1), Term(self.output, -1)])
        return [self.continuity_equation(), eqn1, eqn2]

    def update_properties(self, **kwargs):
        self.k_regain = kwargs.get('Regain coefficient', self.k_regain)
        self.k_loss = kwargs.get('Loss coefficient', self.k_loss)

    def update_solution(self, **kwargs):
        pass
