from poiseuille.components.blocks import PressureReservoir, RestrictorValve
from poiseuille.components.connectors import LinearResistanceConnector
from poiseuille.systems.system import IncompressibleSystem

def run():
    p1 = PressureReservoir(p=10)
    p2 = PressureReservoir(p=0)
    valve = RestrictorValve(max_flow_rate=1)
    c1 = LinearResistanceConnector(r=1)
    c2 = LinearResistanceConnector(r=1.2434)

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