from poiseuille.components.procter_and_gamble.blocks import PressureReservoir, ResistorValve
from poiseuille.components.procter_and_gamble.connector import ProcterAndGambleConnector as Connector
from poiseuille.systems.system import IncompressibleSystem

def run():
    p1 = PressureReservoir(p=1.43)
    p2 = PressureReservoir(p=0)
    c1 = Connector()
    c2 = Connector()
    valve = ResistorValve(r=0.001)

    c1.connect(p1.node, valve.input)
    c2.connect(valve.output, p2.node)

    system = IncompressibleSystem([p1, p2, valve])
    system.solve(verbose=1)

    print(valve.flow_rate, valve.output.p - valve.input.p)

    for node in system.nodes():
        print(node.p, type(node.block))

    for connector in system.connectors():
        print(connector.flow_rate)

if __name__ == '__main__':
    run()