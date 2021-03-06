from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsTextItem

from poiseuille.components.procter_and_gamble.connector import ProcterAndGambleConnector
from poiseuille.ui.dialog import Dialog

class ConnectorGraphisPathItemLabel(QGraphicsTextItem):
    div = '<span style="background-color: white; border-style: solid; border-width: 1px; border-color: red;">{}</span>'

    def __init__(self, parent, name='C'):
        super().__init__(parent)
        self.setHtml(self.div.format(name))
        self.setPos(parent.boundingRect().center())

class ConnectorGraphicsPathItem(QGraphicsPathItem):
    def __init__(self, src_node=None, dest_node=None):
        super(ConnectorGraphicsPathItem, self).__init__()
        self.setFlag(QGraphicsPathItem.ItemIsSelectable)
        self.src_node = src_node
        self.dest_node = dest_node
        self.label = None

    def set_path(self, pt_A, pt_B):
        pts = (
            pt_A,
            QPointF((pt_A.x() + pt_B.x()) / 2., pt_A.y()),
            QPointF((pt_A.x() + pt_B.x()) / 2., pt_B.y()),
            pt_B
        )

        path = QPainterPath(pts[0])
        for pt in pts:
            path.lineTo(pt)

        self.setPath(path)

    def update_path(self):
        if self.src_node and self.dest_node:
            self.set_path(self.src_node.center(), self.dest_node.center())

    def init(self, src_node, dest_node, connector):
        self.connector = connector
        self.src_node = src_node
        self.dest_node = dest_node
        self.src_node.connector = self
        self.dest_node.connector = self
        self.update_path()
        self.label = self.connector.name

    def connect(self, src_node, dest_node):
        if src_node.node.can_connect(dest_node.node):
            self.connector = ProcterAndGambleConnector()
            self.src_node = src_node
            self.dest_node = dest_node
            self.src_node.connector = self
            self.dest_node.connector = self
            self.connector.connect(self.src_node.node, self.dest_node.node)
            self.set_path(self.src_node.center(), self.dest_node.center())
            self.label = ConnectorGraphisPathItemLabel(self, self.connector.name)
            return True

        return False

    def disconnect(self):
        if self.connector:
            self.connector.disconnect()
            self.src_node.connector = None
            self.dest_node.connector = None
            self.src_node = None
            self.dest_node = None
            self.scene().removeItem(self)

    def mouseDoubleClickEvent(self, e):
        dialog = Dialog(self.connector)

        if dialog.exec() == Dialog.Accepted:
            self.connector.update_properties(**dialog.properties())
