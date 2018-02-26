from ..base.block_graphics_item import BlockGraphicsItem
from ..base.node_graphics_item import NodeGraphicsItem
from poiseuille.components.procter_and_gamble.blocks import *


class ProcterAndGambleBlockGraphicsItem(BlockGraphicsItem):
    def __init__(self, block, file):
        super().__init__(block=block, file=file)

    def factory(type, block=None):
        if type == 'Pressure Reservoir':
            return PressureReservoirGraphicsItem(block=block)
        elif type == 'Fan':
            return FanGraphicsItem(block=block)
        elif type == 'Flow Regulator':
            return FlowRegulatorGraphicsItem(block=block)
        elif type == 'Resistor Valve':
            return ResistorValveGraphicsItem(block=block)
        elif type == 'Pressure Valve':
            return PressureValveGraphicsItem(block=block)
        elif type == 'Joiner':
            return JoinerGraphicsItem(block=block)
        else:
            raise ValueError('No block type "{}".'.format(type))

    factory = staticmethod(factory)


class PressureReservoirGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    Block = PressureReservoir

    def __init__(self, block=None):
        super().__init__(block=block if block else PressureReservoir(), file='resources/pressure_reservoir')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.node, self, x=-10, y=17.5))


class FanGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    Block = Fan

    def __init__(self, block=None):
        fan = block
        super().__init__(block=block if block else Fan(), file='resources/fan')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-10, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


class FlowRegulatorGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    Block = FlowRegulator

    def __init__(self, block=None):
        super().__init__(block=block if block else FlowRegulator(), file='resources/const_flow_fan')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-7.5, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


class ResistorValveGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    Block = ResistorValve

    def __init__(self, block=None):
        super().__init__(block=block if block else ResistorValve(), file='resources/valve')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-7.5, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))

class PressureValveGraphicsItem(ResistorValveGraphicsItem):
    Block = PressureValve

    def __init__(self, block=None):
        super().__init__(block=block if block else PressureValve())

class JoinerGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    Block = Joiner

    def __init__(self, block=None):
        super().__init__(block=block if block else Joiner(), file='resources/joiner')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input_1, self, x=-7.5, y=54))
        self.nodes.append(NodeGraphicsItem(self.block.input_2, self, x=-7.5, y=0))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=58, y=26.5))
