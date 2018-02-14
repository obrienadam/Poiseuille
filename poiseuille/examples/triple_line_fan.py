from poiseuille.components.procter_and_gamble.blocks import PressureReservoir, Fan, PerfectSplitter
from poiseuille.components.procter_and_gamble.connector import ProcterAndGambleConnector
from poiseuille.systems.system import IncompressibleSystem

def run():
    p1 = PressureReservoir(p=0)
    p2 = PressureReservoir(p=0)
    p3 = PressureReservoir(p=0)
    fan = Fan(dp=4.3)
    s = PerfectSplitter(num_outputs=2)

    c1 = ProcterAndGambleConnector(diameter=4)
    c2 = ProcterAndGambleConnector(diameter=5)
    c3 = ProcterAndGambleConnector(diameter=6)
    c4 = ProcterAndGambleConnector(diameter=2)

    c1.connect(p1.node, s.input)
    c2.connect(s.outputs[0], p2.node)
    c3.connect(s.outputs[1], fan.input)
    c4.connect(fan.output, p3.node)

    system = IncompressibleSystem([p1, p2, p3, s, fan])
    system.solve()

    for c in c1, c2, c3, c4:
        print(c.flow_rate)
        print()

if __name__ == '__main__':
    run()