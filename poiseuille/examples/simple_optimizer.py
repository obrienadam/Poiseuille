from scipy import optimize as opt
from poiseuille.components.procter_and_gamble.blocks import PressureReservoir, ResistorValve, PerfectJunction, Fan
from poiseuille.components.procter_and_gamble.connector import ProcterAndGambleConnector as Connector
from poiseuille.systems.system import IncompressibleSystem


def run():
    patm = [PressureReservoir(p=0.) for _ in range(4)]
    fan = Fan(dp=0)
    valves = [ResistorValve(r=0) for _ in range(3)]
    joint = PerfectJunction(num_nodes=4)
    conns = [Connector(length=25) for _ in range(8)]

    conns[0].connect(patm[0].node, valves[0].input)
    conns[1].connect(patm[1].node, valves[1].input)
    conns[2].connect(patm[2].node, valves[2].input)
    conns[3].connect(valves[0].output, joint.nodes[0])
    conns[4].connect(valves[1].output, joint.nodes[1])
    conns[5].connect(valves[2].output, joint.nodes[2])
    conns[6].connect(joint.nodes[3], fan.input)
    conns[7].connect(fan.output, patm[3].node)

    system = IncompressibleSystem(patm + [fan] + valves + [joint])
    #system.solve(verbose=1)

    # iters, error = system.solve(max_iters=200, toler=1e-9)

    def obj(x):
        return x[0]**2

    def h1(x):
        callback(x)
        return valves[0].input.connector.flow_rate - 300

    def h2(x):
        callback(x)
        return valves[1].input.connector.flow_rate - 400

    def h3(x):
        callback(x)
        return valves[2].input.connector.flow_rate - 600

    def h4(x):
        return x[1]

    def h5(x):
        return x[2]

    def h6(x):
        return x[3]

    def callback(x):
        dp, r1, r2, r3 = x
        fan.dp = dp
        valves[0].r = r1
        valves[1].r = r2
        valves[2].r = r3
        system.solve(verbose=1, method='bicgstab', maxiter=5000, toler=1e-11)

    constr = [
        {'type': 'eq', 'fun': h1},
        {'type': 'eq', 'fun': h2},
        {'type': 'eq', 'fun': h3},
        {'type': 'ineq', 'fun': h4},
        {'type': 'ineq', 'fun': h5},
        {'type': 'ineq', 'fun': h6}
    ]

    try:
        print(opt.minimize(obj, [0.01, 0, .0, .0], constraints=constr))
    except:
        pass

    print('Objectives')
    print(fan.dp)
    print('Constraints')
    print(valves[0].r)
    print(valves[1].r)
    print(valves[2].r)
    print(valves[0].input.connector.flow_rate)
    print(valves[1].input.connector.flow_rate)
    print(valves[2].input.connector.flow_rate)


if __name__ == '__main__':
    run()
