from PyQt5.QtWidgets import QGraphicsScene

from .block_graphics_item import construct_block

class GraphicsScene(QGraphicsScene):
    def __init__(self, parent):
        super(GraphicsScene, self).__init__(parent=parent)
        print(parent.acceptDrops())

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        e.accept()
        block = construct_block(e.mimeData().text())
        self.addItem(block)