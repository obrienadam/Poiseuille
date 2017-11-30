from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsScene

from .block_graphics_item import construct_block
from .block_graphics_item import NodeGraphicsItem
from .connector_graphics_path_item import ConnectorGraphicsPathItem

class GraphicsScene(QGraphicsScene):
    def __init__(self, parent):
        super(GraphicsScene, self).__init__(parent=parent)
        self.node = None
        self.connector = None

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        e.accept()
        block = construct_block(e.mimeData().text())
        self.addItem(block)
        block.mouseDoubleClickEvent(None)

    def mousePressEvent(self, e):
        item  = self.itemAt(e.scenePos(), QTransform())

        if isinstance(item, NodeGraphicsItem):
            self.node = item
            self.connector = ConnectorGraphicsPathItem()
            self.connector.set_path(item.center(), e.scenePos())
            self.addItem(self.connector)
            e.accept()
        else:
            super(GraphicsScene, self).mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self.connector:
            self.connector.set_path(self.node.center(), e.scenePos())
            e.accept()
        else:
            super(GraphicsScene, self).mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if self.connector:
            e.accept()

            for item in self.items(e.scenePos()):
                if isinstance(item, NodeGraphicsItem) and self.connector.connect(self.node, item):
                    self.connector = None
                    return


            self.removeItem(self.connector)
            self.connector = None
        else:
            super(GraphicsScene, self).mouseReleaseEvent(e)