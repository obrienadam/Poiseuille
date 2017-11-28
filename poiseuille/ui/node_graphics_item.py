from PyQt5 import QtWidgets

from poiseuille.components.nodes import Node

class NodeGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, node=None, block_graphics_item=None):
        self.node = node
        super(NodeGraphicsItem, self).__init__(parent=block)