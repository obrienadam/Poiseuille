from scipy import optimize as opt
from poiseuille.components.procter_and_gamble import PressureReservoir, ConstantDeliveryFan, PerfectJunction, Fan
from poiseuille.components.procter_and_gamble import ProcterAndGambleConnector as Connector
from poiseuille.systems.system import IncompressibleSystem


def run():
    patm = [PressureReservoir(p=0.) for _ in range(4)]
    fan = Fan(dp=4)
    valves = [ConstantDeliveryFan() for _ in range(3)]
    joint = PerfectJunction(num_nodes=4)
    conns = [Connector(diameter=7.32, length=25) for _ in range(8)]

    valves[0].flow_rate = 300
    valves[1].flow_rate = 400
    valves[2].flow_rate = 550

    conns[0].connect(patm[0].node, valves[0].input)
    conns[1].connect(patm[1].node, valves[1].input)
    conns[2].connect(patm[2].node, valves[2].input)
    conns[3].connect(valves[0].output, joint.nodes[0])
    conns[4].connect(valves[1].output, joint.nodes[1])
    conns[5].connect(valves[2].output, joint.nodes[2])
    conns[6].connect(joint.nodes[3], fan.input)
    conns[7].connect(fan.output, patm[3].node)

    system = IncompressibleSystem(patm + [fan] + valves + [joint])
    system.solve(verbose=1)

    # iters, error = system.solve(max_iters=200, toler=1e-9)

    def obj(x):
        return x[0]**2

    def h1(x):
        callback(x)
        return -valves[0].dp

    def h2(x):
        callback(x)
        return -valves[1].dp

    def h3(x):
        callback(x)
        return -valves[2].dp

    def callback(x):
        fan.dp = x[0]
        system.solve(verbose=1, method='bicgstab', maxiter=200, toler=1e-12)

    constr = [
        {'type': 'ineq', 'fun': h1},
        {'type': 'ineq', 'fun': h2},
        {'type': 'ineq', 'fun': h3},
    ]

    try:
        print(opt.minimize(obj, [fan.dp, 1, 1, 1], constraints=constr))
    except:
        pass

    print('Objectives')
    print(fan.dp)
    print('Constraints')
    print(valves[0].dp)
    print(valves[1].dp)
    print(valves[2].dp)


if __name__ == '__main__':
    run()
