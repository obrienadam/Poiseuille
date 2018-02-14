from poiseuille.components.procter_and_gamble.blocks import PressureReservoir
from poiseuille.components.procter_and_gamble.connector import ProcterAndGambleConnector as Connector
from poiseuille.systems.system import IncompressibleSystem


def run():
    p1 = PressureReservoir(p=(1.11))
    p2 = PressureReservoir(p=0.)
    c = Connector(k_ent=1.324)
    c.connect(p1.node, p2.node)

    system = IncompressibleSystem([p1, p2])

    system.solve(toler=1e-14, verbose=1)

    for connector in system.connectors():
        print(connector.flow_rate)


if __name__ == '__main__':
    run()
