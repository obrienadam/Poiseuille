from ..base.block_graphics_item import BlockGraphicsItem
from ..base.node_graphics_item import NodeGraphicsItem
from poiseuille.components.procter_and_gamble.blocks import *

class ProcterAndGambleBlockGraphicsItem(BlockGraphicsItem):
    def __init__(self, block, file):
        super().__init__(block=block, file=file)

    def factory(type):
        if type == 'Pressure Reservoir':
            return PressureReservoirGraphicsItem()
        elif type == 'Fan':
            return FanGraphicsItem()
        elif type == 'Constant Delivery Fan':
            return ConstDeliveryFanGraphicsItem()
        elif type == 'Restrictor Valve':
            return RestrictorValveGraphicsItem()
        elif type == 'Joiner':
            return JoinerGraphicsItem()
        else:
            raise ValueError('No block type "{}".'.format(type))

    factory = staticmethod(factory)

class PressureReservoirGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    def __init__(self):
        super().__init__(block=PressureReservoir(), file='resources/pressure_reservoir')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.node, self, x=-10, y=17.5))


class FanGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    def __init__(self):
        super().__init__(block=Fan(), file='resources/fan')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-10, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


class ConstDeliveryFanGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    def __init__(self):
        super().__init__(block=ConstantDeliveryFan(), file='resources/const_flow_fan')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-7.5, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


class RestrictorValveGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    def __init__(self):
        super().__init__(block=RestrictorValve(), file='resources/valve')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-7.5, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


class JoinerGraphicsItem(ProcterAndGambleBlockGraphicsItem):
    def __init__(self):
        super().__init__(block=Joiner(), file='resources/joiner')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input_1, self, x=-7.5, y=54))
        self.nodes.append(NodeGraphicsItem(self.block.input_2, self, x=-7.5, y=0))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=58, y=26.5))