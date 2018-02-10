from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsScene

from ..ui import base
from ..ui import procter_and_gamble

class GraphicsScene(QGraphicsScene):
    def __init__(self, parent, block_list=None, connector_list=None):
        super().__init__(parent=parent)
        self.block_list = block_list
        self.connector_list = connector_list
        self.node = None
        self.connector = None

    def blocks(self):
        return [item.block for item in self.items() if isinstance(item, base.BlockGraphicsItem)]

    def blocks_of_type(self, Block):
        return [item.block for item in self.blockGraphicsItems() if isinstance(item.block, Block)]

    def connectors(self):
        return [item.connector for item in self.items() if isinstance(item, base.ConnectorGraphicsPathItem)]

    def num_blocks(self):
        return sum(isinstance(item, base.BlockGraphicsItem) for item in self.items())

    def num_connectors(self):
        return sum(isinstance(item, base.ConnectorGraphicsPathItem) for item in self.items())

    def load(self, blocks, positions):
        self.clear()

        for block, pos in zip(blocks, positions):
            item = procter_and_gamble.ProcterAndGambleBlockGraphicsItem.factory(block.type(), block)
            item.setPos(*pos)
            self.addItem(item)

        # Get map of nodes to their graphic items
        node_to_graphics_item = {}

        for block in self.blockGraphicsItems():
            for node in block.nodes:
                node_to_graphics_item[node.node] = node

        # Construct connector list
        connectors = []

        for block in blocks:
            for node in block.nodes:
                conn = node.connector

                if conn and not conn in connectors:
                    src = node_to_graphics_item[conn.input]
                    dest = node_to_graphics_item[conn.output]
                    item = base.ConnectorGraphicsPathItem()
                    item.init(src, dest, conn)
                    self.addItem(item)
                    connectors.append(conn)

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        e.accept()
        block = procter_and_gamble.ProcterAndGambleBlockGraphicsItem.factory(e.mimeData().text())
        block.setPos(e.scenePos())
        self.addItem(block)

        if self.block_list:
            pass

        block.mouseDoubleClickEvent(None)

    def mousePressEvent(self, e):
        item  = self.itemAt(e.scenePos(), QTransform())

        if isinstance(item, base.NodeGraphicsItem) and not item.connector:
            self.node = item
            self.connector = base.ConnectorGraphicsPathItem()
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
                if isinstance(item, base.NodeGraphicsItem) and self.connector.connect(self.node, item):
                    if self.connector_list:
                        pass

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

                if isinstance(item, base.BlockGraphicsItem):
                    self.removeItem(item)

        super().keyPressEvent(e)