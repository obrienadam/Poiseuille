import numpy as np
import numpy.linalg as la

from poiseuille.components.procter_and_gamble.blocks import PressureReservoir, PowerCurveFan
from poiseuille.components.procter_and_gamble.connector import ProcterAndGambleConnector as Connector
from poiseuille.systems.system import IncompressibleSystem


def run():
    A = np.mat([
        [0, 0, 1],
        [500 ** 2, 500, 1],
        [1000 ** 2, 1000, 1]
    ])

    x = np.array(
        [0, 1.01, 3]
    )

    c = la.solve(A, x)

    power_curve = lambda q: c[0] * q ** 2 + c[1] * q + c[2]

    p1 = PressureReservoir(p=0.2)
    p2 = PressureReservoir(p=0)
    fan = PowerCurveFan(fcn=power_curve)
    c1 = Connector()
    c2 = Connector()
    c1.connect(p1.node, fan.input)
    c2.connect(fan.output, p2.node)

    fan.update_properties()

    system = IncompressibleSystem([p1, p2, fan])
    system.solve(verbose=1)

    for c in system.connectors():
        print(c.flow_rate)

    print(fan.dp, fan.flow_rate)


run()
