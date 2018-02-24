from scipy import optimize as opt
from poiseuille.components.procter_and_gamble.blocks import PressureReservoir, ResistorValve, PerfectJunction, Fan
from poiseuille.components.procter_and_gamble.connector import ProcterAndGambleConnector as Connector
from poiseuille.systems.system import IncompressibleSystem
from poiseuille.optimizers import Optimizer


def run():
    patm = [PressureReservoir(p=0.) for _ in range(4)]
    fan = Fan(dp=0)
    valves = [ResistorValve(r=0) for _ in range(3)]
    joint = PerfectJunction(num_nodes=4)
    conns = [Connector(length=25, diameter=1 + i) for i in range(8)]

    conns[0].connect(patm[0].node, valves[0].input)
    conns[1].connect(patm[1].node, valves[1].input)
    conns[2].connect(patm[2].node, valves[2].input)
    conns[3].connect(valves[0].output, joint.nodes[0])
    conns[4].connect(valves[1].output, joint.nodes[1])
    conns[5].connect(valves[2].output, joint.nodes[2])
    conns[6].connect(joint.nodes[3], fan.input)
    conns[7].connect(fan.output, patm[3].node)

    system = IncompressibleSystem(patm + [fan] + valves + [joint])

    optimizer = Optimizer(system=system)

    optimizer.init_objective_function(blocks=[fan], var='dp')

    for i, v in enumerate(valves):
        optimizer.add_property_constraint(v, 'Resistance', 'ineq', 0.)
        optimizer.add_solution_constraint(v, 'Flow rate', 'eq', 130 + 12 * i)

    optimizer.optimize(guess=[1, 0, 0, 0])

    print('Objectives')
    print(fan.dp)
    print('Constraints')
    print(valves[0].r)
    print(valves[1].r)
    print(valves[2].r)
    print(valves[0].flow_rate)
    print(valves[1].flow_rate)
    print(valves[2].flow_rate)
    print(system.status)


if __name__ == '__main__':
    run()
