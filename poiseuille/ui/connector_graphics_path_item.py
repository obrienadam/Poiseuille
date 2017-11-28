from PyQt5 import QtWidgets, QtGui, QtCore

from poiseuille.components.connectors import Connector


class ConnectorGraphicsPathItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, src_node, dest_node=None, connector_type=None):
        super(ConnectorGraphicsPathItem, self).__init__()
        self.src_node = src_node
        self.dest_node = dest_node

    def setPathTo(self, pt):
        start = self.src_node.mapToScene(self.src_node.boundingRect().center())
        pts = [QtCore.QPointF((start.x() + pt.x()) / 2., start.y()), QtCore.QPointF((start.x() + pt.x()) / 2., pt.y()), pt]

        path = QtGui.QPainterPath(start)
        for pt in pts:
            path.lineTo(pt)

        self.setPath(path)

    def update_path(self):
        s = self.src_node.mapToScene(self.src_node.boundingRect().center())
        d = self.dest_node.mapToScene(self.dest_node.boundingRect().center())

        pts = [
            s,
            QtCore.QPointF((s.x() + d.x()) / 2., s.y()),
            QtCore.QPointF((s.x() + d.x()) / 2., d.y()),
            d
        ]

        path = QtGui.QPainterPath(s)

        for pt in pts[1:]:
            path.lineTo(pt)

        self.setPath(path)

    def connect(self, dest_node):
        if self.src_node.node.can_connect(dest_node.node):
            self.connector = Connector()
            self.dest_node = dest_node
            self.dest_node.connector = self
            self.connector.connect(self.src_node.node, self.dest_node.node)
            return True

        return False
