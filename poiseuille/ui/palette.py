from PyQt5.QtWidgets import QPushButton, QSizePolicy, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QDrag
from PyQt5.QtCore import QSize, QByteArray, QMimeData

class BlockPaletteItem(QLabel):
    def __init__(self, block, parent=None):
        super(BlockPaletteItem, self).__init__(parent=parent)
        self.block = block()
        self.setPixmap(self.block.pixmap())
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def mousePressEvent(self, e):
        drag = QDrag(self)
        drag.setPixmap(self.pixmap())

        mimeData = QMimeData()
        mimeData.setText(self.block.block.TYPE)

        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos())
        drag.exec()