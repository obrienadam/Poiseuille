from PyQt5 import QtCore, QtGui, QtWidgets

class BlockPaletteItem(QtWidgets.QLabel):
    def __init__(self, BlockGraphicsItem, parent=None):
        super(BlockPaletteItem, self).__init__(parent=parent)
        self.block = BlockGraphicsItem()
        self.setPixmap(self.block.pixmap())
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    def mousePressEvent(self, e):
        drag = QtGui.QDrag(self)
        drag.setPixmap(self.pixmap())

        mimeData = QtCore.QMimeData()
        mimeData.setText(self.block.block.type())

        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos())
        drag.exec()