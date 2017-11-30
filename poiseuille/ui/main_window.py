from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QTreeWidget, QHBoxLayout, QGraphicsView
from PyQt5 import uic

from .graphics_scene import GraphicsScene
from .block_graphics_item import *
from .palette import BlockPaletteItem

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('designer/mainwindow.ui', self)

        view = self.graphics_view
        scene = GraphicsScene(view)
        view.setScene(scene)

        self.init_parameters_tree()
        self.init_palettes()
        self.show()

    def init_parameters_tree(self):
        pass

    def init_palettes(self):
        self.palette_env.setLayout(QHBoxLayout())
        self.palette_power.setLayout(QHBoxLayout())
        self.palette_valves.setLayout(QHBoxLayout())

        self.palette_env.layout().addWidget(BlockPaletteItem(block=PressureReservoirGraphicsItem))
        self.palette_power.layout().addWidget(BlockPaletteItem(block=FanGraphicsItem))
        self.palette_power.layout().addWidget(BlockPaletteItem(block=ConstFlowFanGraphicsItem))
        self.palette_valves.layout().addWidget(BlockPaletteItem(block=RestrictorValveGraphicsItem))