from poiseuille.components.blocks import PressureReservoir, Fan, PerfectSplitter
from poiseuille.components.connector import Connector
from poiseuille.components.resistance_functions import ProctorAndGambleResistance
from poiseuille.systems.system import IncompressibleSystem

def run():
    p1 = PressureReservoir(p=0)
    p2 = PressureReservoir(p=0)
    p3 = PressureReservoir(p=0)
    fan = Fan(dp=4.3)
    s = PerfectSplitter(num_outputs=2)

    c1 = Connector(r_func=ProctorAndGambleResistance(d=5, l=50))
    c2 = Connector(r_func=ProctorAndGambleResistance(d=5, l=50))
    c3 = Connector(r_func=ProctorAndGambleResistance(d=5, l=50))
    c4 = Connector(r_func=ProctorAndGambleResistance(d=5, l=50))

    c1.connect(p1.node, s.input)
    c2.connect(s.outputs[0], p2.node)
    c3.connect(s.outputs[1], fan.input)
    c4.connect(fan.output, p3.node)

    system = IncompressibleSystem([p1, p2, p3, s, fan])
    system.solve()

if __name__ == '__main__':
    run()