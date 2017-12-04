from poiseuille.components.blocks import PressureReservoir, ResistorValve, PerfectJunction, Fan
from poiseuille.components.connectors import ProctorAndGambleConnector
from poiseuille.systems.system import IncompressibleSystem

from scipy import optimize as opt


def run():
    p = [PressureReservoir(p=0.) for i in range(5)]
    j = PerfectJunction(num_nodes=5)
    f = [Fan(dp=3), Fan(dp=3)]
    v = [ResistorValve(r=0.), ResistorValve(r=0.)]
    c = [ProctorAndGambleConnector(d=3 + i % 2, l=25 + i) for i in range(9)]

    c[0].connect(p[0].node, v[0].input)
    c[1].connect(p[1].node, v[1].input)
    c[2].connect(v[0].output, f[0].input)
    c[3].connect(v[1].output, j.nodes[0])
    c[4].connect(f[0].output, j.nodes[1])
    c[5].connect(p[2].node, f[1].output)
    c[6].connect(f[1].input, j.nodes[2])
    c[7].connect(j.nodes[3], p[3].node)
    c[8].connect(j.nodes[4], p[4].node)

    system = IncompressibleSystem(p + [j] + f + v)

    # iters, error = system.solve(max_iters=200, toler=1e-9)

    def obj(x):
        return x[0] ** 2 + x[1] ** 2

    def h1(x):
        callback(x)
        return v[0].input.connector.flow_rate - 100

    def h2(x):
        callback(x)
        return v[1].input.connector.flow_rate - 100

    def h3(x):
        return x[2]

    def h4(x):
        return x[3]

    def h5(x):
        return x[0]

    def h6(x):
        return x[1]

    def callback(x):
        dp1, dp2, r1, r2 = x
        f[0].dp = dp1
        f[1].dp = dp2
        v[0].r = r1
        v[1].r = r2
        system.solve()

    constr = [
        {'type': 'eq', 'fun': h1},
        {'type': 'eq', 'fun': h2},
        {'type': 'ineq', 'fun': h3},
        {'type': 'ineq', 'fun': h4},
        # {'type': 'ineq', 'fun': h6}
    ]

    print(opt.minimize(obj, [1, 1, 0, 0], constraints=constr))

    print('Objectives')
    print(f[0].input.connector.flow_rate)
    print(f[1].input.connector.flow_rate)
    print(v[0].input.connector.flow_rate)
    print(v[1].input.connector.flow_rate)
    print('All connectors')
    for conn in c:
        print(conn.flow_rate)


if __name__ == '__main__':
    run()
