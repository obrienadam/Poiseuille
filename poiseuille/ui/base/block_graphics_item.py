from PyQt5 import QtWidgets, QtCore, QtGui

from poiseuille.ui.dialog import BlockDialog

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

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)

        for item in self.scene().selectedItems():
            if isinstance(item, BlockGraphicsItem):
                for node in item.nodes:
                    if node.connector:
                        node.connector.update_path()

