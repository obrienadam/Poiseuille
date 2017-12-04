from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsScene

from .block_graphics_item import construct_block, BlockGraphicsItem
from .block_graphics_item import NodeGraphicsItem
from .connector_graphics_path_item import ConnectorGraphicsPathItem

class GraphicsScene(QGraphicsScene):
    def __init__(self, parent, ConnectorType):
        super(GraphicsScene, self).__init__(parent=parent)
        self.ConnectorType = ConnectorType
        self.node = None
        self.connector = None

    def blocks(self):
        return [item.block for item in self.blockGraphicsItems()]

    def blockGraphicsItems(self):
        return [item for item in self.items() if isinstance(item, BlockGraphicsItem)]

    def connectors(self):
        return [item.connector for item in self.items() if isinstance(item, ConnectorGraphicsPathItem)]

    def num_blocks(self):
        return sum(isinstance(item, BlockGraphicsItem) for item in self.items())

    def num_connectors(self):
        return sum(isinstance(item, ConnectorGraphicsPathItem) for item in self.items())

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        e.accept()
        block = construct_block(e.mimeData().text())
        block.setPos(e.scenePos())
        self.addItem(block)
        block.mouseDoubleClickEvent(None)

    def mousePressEvent(self, e):
        item  = self.itemAt(e.scenePos(), QTransform())

        if isinstance(item, NodeGraphicsItem) and not item.connector:
            self.node = item
            self.connector = ConnectorGraphicsPathItem(connector_type=self.ConnectorType)
            self.connector.set_path(item.center(), e.scenePos())
            self.addItem(self.connector)
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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                item.disconnect()

                if isinstance(item, BlockGraphicsItem):
                    self.removeItem(item)

        super().keyPressEvent(e)