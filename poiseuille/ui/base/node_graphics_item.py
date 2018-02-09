from PyQt5 import QtWidgets

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