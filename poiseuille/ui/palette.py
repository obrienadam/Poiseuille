from PyQt5.QtWidgets import QSizePolicy, QLabel, QScrollArea, QGridLayout, QGraphicsTextItem
from PyQt5.QtGui import QDrag, QPalette, QColor, QPixmap, QPainter, QFont, QImage, QTextFrame
from PyQt5.QtCore import QMimeData, Qt, QRect, QPoint

class BlockPaletteItem(QLabel):
    def __init__(self, Block, parent=None):
        super().__init__(parent=parent)
        self.block = Block()
        self.block.block.name = self.block.block.TYPE

        pixmap = self.block.pixmap()
        label = QGraphicsTextItem(self.block.block.TYPE)

        img = QImage(max(pixmap.width(), label.textWidth()), pixmap.height() + 22, QImage.Format_ARGB32)
        img.fill(QColor(255, 255, 255, 0))

        painter = QPainter(img)
        painter.setFont(QFont('Arial'))

        if label.textWidth() > pixmap.width():
            painter.drawPixmap(label.textWidth() / 2 - pixmap.width() / 2, 0, pixmap)
            painter.drawText(0, pixmap.height() + 16, label.toPlainText())
        else:
            painter.drawPixmap(0, 0, pixmap)
            painter.drawText(0, pixmap.height() + 16, label.toPlainText())

        painter.end()

        self.setPixmap(QPixmap.fromImage(img))


    def mousePressEvent(self, e):
        drag = QDrag(self)
        drag.setPixmap(self.pixmap())

        mimeData = QMimeData()
        mimeData.setText(self.block.block.TYPE)

        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos())
        drag.exec()

class BlockPalette(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        p = QPalette()
        p.setColor(QPalette.Window, QColor(255, 255, 255))
        self.setPalette(p)

        self.grid = QGridLayout()

        self.setLayout(self.grid)

        self.row = 0
        self.col = 0

    def add_block_type(self, Block):
        item = BlockPaletteItem(Block=Block)
        #self.grid.setColumnMinimumWidth(self.col, max(self.grid.columnMinimumWidth(self.col), item.width()))
        self.grid.addWidget(item, self.row, self.col, Qt.AlignTop | Qt.AlignLeft)

        if self.col == 2:
            self.row += 1
            self.col = 0
        else:
            self.col += 1
