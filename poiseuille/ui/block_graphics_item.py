from PyQt5 import QtWidgets, QtCore, QtGui

from poiseuille.components.blocks import *

from .dialog import BlockDialog
from .connector_graphics_path_item import ConnectorGraphicsPathItem


class NodeGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, node, block, x=0, y=0):
        super().__init__(x, y, 10, 10, parent=block)
        self.node = node
        self.block = block
        self.connector = None

    def disconnect(self):
        if self.connector:
            self.connector.disconnect()

    def center(self):
        return self.mapToScene(self.boundingRect().center())


class BlockGraphicsItemLabel(QtWidgets.QGraphicsTextItem):
    def __init__(self, parent):
        super(BlockGraphicsItemLabel, self).__init__(parent=parent)
        self.setTextInteractionFlags(QtCore.Qt.TextEditable)
        self.setPlainText(parent.block.name)
        self.setPos(parent.boundingRect().bottomLeft())

    def paint(self, painter, style, widget):
        self.parentItem().block.name = self.toPlainText()
        wp = self.parentItem().boundingRect().width()
        w = self.boundingRect().width()
        self.setPos(QtCore.QPointF((wp - w) / 2., self.pos().y()))

        return super().paint(painter, style, widget)


class BlockGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, block=None, file='resources/default'):
        super().__init__(QtGui.QPixmap(file), None)
        self.block = block
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.init_label()
        self.nodes = []
        self.init_nodes()

    def init_label(self):
        self.label = BlockGraphicsItemLabel(self)

    def init_nodes(self):
        raise NotImplementedError('Block graphics items must implement node placement.')

    def disconnect(self):
        for node in self.nodes:
            node.disconnect()

    def mouseDoubleClickEvent(self, QGraphicsSceneMouseEvent):
        dialog = BlockDialog(self.block)

        if dialog.exec() == BlockDialog.Accepted:
            self.block.update_properties(**dialog.properties())

    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        super(BlockGraphicsItem, self).mouseMoveEvent(QGraphicsSceneMouseEvent)

        for node in self.nodes:
            if node.connector:
                node.connector.update_path()


class PressureReservoirGraphicsItem(BlockGraphicsItem):
    def __init__(self, block=PressureReservoir()):
        super(PressureReservoirGraphicsItem, self).__init__(block=block, file='resources/pressure_reservoir')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.node, self, x=-10, y=17.5))


class FanGraphicsItem(BlockGraphicsItem):
    def __init__(self, block=Fan()):
        super(FanGraphicsItem, self).__init__(block=block, file='resources/fan')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-10, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


class ConstFlowFanGraphicsItem(BlockGraphicsItem):
    def __init__(self, block=ConstantDeliveryFan()):
        super(ConstFlowFanGraphicsItem, self).__init__(block=block, file='resources/const_flow_fan')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-7.5, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


class RestrictorValveGraphicsItem(BlockGraphicsItem):
    def __init__(self, block=RestrictorValve()):
        super(RestrictorValveGraphicsItem, self).__init__(block=block, file='resources/valve')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-7.5, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


def construct_block(type):
    if type == 'Pressure Reservoir':
        return PressureReservoirGraphicsItem(block=PressureReservoir())
    elif type == 'Fan':
        return FanGraphicsItem(block=Fan())
    elif type == 'Constant Delivery Fan':
        return ConstFlowFanGraphicsItem(block=ConstantDeliveryFan())
    elif type == 'Restrictor Valve':
        return RestrictorValveGraphicsItem(block=RestrictorValve())
    else:
        raise ValueError('Unrecognized block type "{}".'.format(type))
