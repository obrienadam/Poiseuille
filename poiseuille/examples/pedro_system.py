from poiseuille.components.blocks import PressureReservoir, ResistorValve, PerfectJunction, Fan
from poiseuille.components.connectors import LinearResistanceConnector
from poiseuille.systems.system import IncompressibleSystem
from random import random

p1 = PressureReservoir(p=0.)
p2 = PressureReservoir(p=0.)
p3 = PressureReservoir(p=0.)
v1 = ResistorValve(r=1)
v2 = ResistorValve(r=1)
junc = PerfectJunction(num_nodes=3)
fan = Fan(dp=1)
conns = [LinearResistanceConnector(0.1) for i in range(6)]
conns[0].connect(p1.node, v1.input)
conns[1].connect(p2.node, v2.input)
conns[2].connect(v1.output, junc.nodes[0])
conns[3].connect(v2.output, junc.nodes[1])
conns[4].connect(junc.nodes[2], fan.input)
conns[5].connect(fan.output, p3.node)
solver = IncompressibleSystem([p1, p2, p3, v1, v2, junc, fan])

def run():
    def func(x):
        dp, r1, r2, r3, r4 = x
        return dp

    def h1(x):
        dp, r1, r2, r3, r4 = x
        r = r2 + 0.003
        q = dp / r
        return q - 0.5

    def h2(x):
        dp, r1, r2, r3, r4 = x
        r = r1 + 0.012
        q = dp / r
        return q - 0.3

    def h3(x):
        dp, r1, r2, r3, r4 = x
        r = r3 + 0.003544
        q = dp / r
        return q - 0.5

    def h4(x):
        dp, r1, r2, r3, r4 = x
        r = r4 + 0.012643
        q = dp / r
        return q - 0.000534

    def h5(x):
        dp, r1, r2, r3, r4 = x
        return r1

    def h6(x):
        dp, r1, r2, r3, r4 = x
        return r2

    def h7(x):
        dp, r1, r2, r3, r4 = x
        return r3

    def h8(x):
        dp, r1, r2, r3, r4 = x
        return r4

    from scipy.optimize import minimize

    constraints = [
        {'type': 'eq', 'fun': h1},
        {'type': 'eq', 'fun': h2},
        {'type': 'eq', 'fun': h3},
        {'type': 'eq', 'fun': h4},
        {'type': 'ineq', 'fun': h5},
        {'type': 'ineq', 'fun': h6},
        {'type': 'ineq', 'fun': h7},
        {'type': 'ineq', 'fun': h8},
    ]

    r = minimize(func, [0.145, 0, 0, 0, 0], constraints=constraints, method='SLSQP', tol=1e-14, options={'maxiter': 10000})

    print(r)

    print(v1.r)
    print(v2.r)
    print(fan.input.connector.flow_rate)
    print(v1.input.connector.flow_rate)
    print(v2.input.connector.flow_rate)

if __name__ == '__main__':
    run()