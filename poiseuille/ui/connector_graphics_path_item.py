from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QGraphicsPathItem

from poiseuille.components.connectors import Connector


class ConnectorGraphicsPathItem(QGraphicsPathItem):
    def __init__(self, src_node=None, dest_node=None, connector_type=None):
        super(ConnectorGraphicsPathItem, self).__init__()
        self.src_node = src_node
        self.dest_node = dest_node

    def set_path(self, pt_A, pt_B):
        pts = [
            pt_A,
            QPointF((pt_A.x() + pt_B.x()) / 2., pt_A.y()),
            QPointF((pt_A.x() + pt_B.x()) / 2., pt_B.y()),
            pt_B
        ]

        path = QPainterPath(pts[0])
        for pt in pts:
            path.lineTo(pt)

        self.setPath(path)

    def update_path(self):
        if self.src_node and self.dest_node:
            self.set_path(self.src_node.center(), self.dest_node.center())

    def connect(self, src_node, dest_node):
        if src_node.node.can_connect(dest_node.node):
            self.connector = Connector()
            self.src_node = src_node
            self.dest_node = dest_node
            self.src_node.connector = self
            self.dest_node.connector = self
            self.connector.connect(self.src_node.node, self.dest_node.node)
            self.set_path(self.src_node.center(), self.dest_node.center())
            return True

        return False
