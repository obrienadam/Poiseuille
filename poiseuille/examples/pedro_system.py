from poiseuille.components.blocks import PressureReservoir, RestrictorValve, PerfectJunction, Fan
from poiseuille.components.connectors import ProctorAndGambleConnector
from poiseuille.systems.system import IncompressibleSystem

def run():
    p = [PressureReservoir(p=0.) for i in xrange(5)]
    j = PerfectJunction(num_nodes=5)
    f = [Fan(dp=4.), Fan(dp=3.984)]
    c = [ProctorAndGambleConnector(d=3+i%2, l=25+i) for i in xrange(7)]

    c[0].connect(p[0].node, j.nodes[0])
    c[1].connect(p[1].node, j.nodes[1])
    c[2].connect(p[2].node, j.nodes[2])
    c[3].connect(j.nodes[3], f[0].input)
    c[4].connect(f[0].output, p[3].node)
    c[5].connect(j.nodes[4], f[1].input)
    c[6].connect(f[1].output, p[4].node)

    system = IncompressibleSystem(p + [j] + f)
    iters, error = system.solve(max_iters=100)

    print iters, error

    for c in system.connectors():
        print c.flow_rate

if __name__ == '__main__':
    run()