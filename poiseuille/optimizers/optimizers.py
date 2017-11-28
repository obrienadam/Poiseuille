class Optimizer(object):
    def __init__(self, system=None):
        self.system = system

    def optimize(self):
        raise NotImplementedError

class SingleFanOptimizer(Optimizer):
    def __init__(self, system=None, fan=None, valves=[]):
        super(SingleFanOptimizer, self).__init__(system=system)
        self.fan = fan
        self.valves = valves

    def optimize(self):
        error = max([abs(valve.flow_rate - valve.max_flow_rate) for valve in self.valves])
        resistance = min([valve.r for valve in self.valves])

        