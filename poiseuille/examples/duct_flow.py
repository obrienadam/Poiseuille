from poiseuille.components.procter_and_gamble.blocks import PressureReservoir
from poiseuille.components.procter_and_gamble.connector import Connector
from poiseuille.components.resistance_functions import ProctorAndGambleResistance
from poiseuille.systems.system import IncompressibleSystem

def run():
    p1 = PressureReservoir(p=(1.44+5.6))
    p2 = PressureReservoir(p=0.)
    c = Connector(r_func=ProctorAndGambleResistance(l=50, d=5, k_ent=1.42))
    c.connect(p1.node, p2.node)

    system = IncompressibleSystem([p1, p2])

    system.solve(toler=1e-14, verbose=1)

    for connector in system.connectors():
        print(connector.flow_rate)

if __name__ == '__main__':
    run()