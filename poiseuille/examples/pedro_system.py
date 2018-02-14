from scipy import optimize as opt
from poiseuille.components.procter_and_gamble.blocks import PressureReservoir, ResistorValve, PerfectJunction, Fan
from poiseuille.components.procter_and_gamble.connector import ProcterAndGambleConnector as Connector
from poiseuille.systems.system import IncompressibleSystem


def run():
    p = [PressureReservoir(p=0.) for i in range(5)]
    j = PerfectJunction(num_nodes=5)
    f = [Fan(dp=1), Fan(dp=1), Fan(dp=1)]
    v = [ResistorValve(r=0.), ResistorValve(r=0.)]
    c = [Connector(diameter=6, length=25) for i in range(10)]
    #c = [LinearResistanceConnector(r=0.01) for i in range(10)]

    c[0].connect(p[0].node, v[0].input)
    c[1].connect(p[1].node, v[1].input)
    c[2].connect(v[0].output, f[0].input)
    c[3].connect(v[1].output, j.nodes[0])
    c[4].connect(f[0].output, j.nodes[1])
    c[5].connect(p[2].node, f[1].output)
    c[6].connect(f[1].input, j.nodes[2])
    c[7].connect(j.nodes[3], p[3].node)
    c[8].connect(j.nodes[4], f[2].input)
    c[9].connect(f[2].output, p[4].node)

    system = IncompressibleSystem(p + [j] + f + v)

    # system.solve(verbose=1, method='gmres')
    # iters, error = system.solve(max_iters=200, toler=1e-9)

    def obj(x):
        return x[0] ** 2 + x[1] ** 2 + x[2] ** 2

    def h1(x):
        callback(x)
        return v[0].input.connector.flow_rate - 450

    def h2(x):
        callback(x)
        return v[1].input.connector.flow_rate - 340

    def h3(x):
        return x[3]

    def h4(x):
        return x[4]

    def h5(x):
        return 2 - abs(x[0] - x[1])

    def h6(x):
        return 2 - abs(x[1] - x[2])

    def callback(x):
        f[0].dp = x[0]
        f[1].dp = x[1]
        f[2].dp = x[2]
        v[0].r = x[3]
        v[1].r = x[4]
        system.solve(verbose=1, method='lgmres', maxiter=1000)

    constr = [
        {'type': 'eq', 'fun': h1},
        {'type': 'eq', 'fun': h2},
        {'type': 'ineq', 'fun': h3},
        {'type': 'ineq', 'fun': h4},
        {'type': 'ineq', 'fun': h5},
        {'type': 'ineq', 'fun': h6},
    ]

    print(opt.minimize(obj, [f[0].dp, f[1].dp, f[2].dp, 0, 0], constraints=constr))

    print('Objectives')
    print(f[0].dp)
    print(f[1].dp)
    print(f[2].dp)
    print('Constraints')
    print(v[0].input.connector.flow_rate)
    print(v[1].input.connector.flow_rate)
    print('All connectors')
    for conn in c:
        print(conn.flow_rate)


if __name__ == '__main__':
    run()
