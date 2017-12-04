import pickle

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QAction, QToolBar, QTreeWidget
from PyQt5 import uic

from .graphics_scene import GraphicsScene
from .block_graphics_item import *
from .palette import BlockPaletteItem

from poiseuille.systems.system import IncompressibleSystem
from poiseuille.components.connectors import LinearResistanceConnector, ProctorAndGambleConnector

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(uifile='designer/mainwindow.ui', baseinstance=self)

        view = self.graphics_view
        scene = GraphicsScene(view, LinearResistanceConnector)
        view.setScene(scene)

        self.init_parameters_tree()
        self.init_palettes()
        self.init_actions()
        self.loaded_case = None
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

    def init_actions(self):
        self.solver_params = self.parameters_tree.topLevelItem(0).child(0)
        self.fluid_params = self.parameters_tree.topLevelItem(0).child(1)
        self.solver_params_widget = self.main_tab_widget.widget(1)
        self.fluid_params_widget = self.main_tab_widget.widget(2)

        self.main_tab_widget.removeTab(1)
        self.main_tab_widget.removeTab(1)

        # Parameter tree
        self.parameters_tree.itemDoubleClicked.connect(self.change_params)

        # Toolbar
        self.toolBar.actions()[0].triggered.connect(self.run_sim)

        # Menu
        actions = self.menuFile.actions()
        actions[0].triggered.connect(self.on_actionNew)
        actions[1].triggered.connect(self.on_actionOpen)
        actions[2].triggered.connect(self.on_actionSave)
        actions[3].triggered.connect(self.on_actionSaveAs)

    def on_actionNew(self):
        pass

    def on_actionOpen(self):
        with open('case.poi', 'rb') as f:
            items = pickle.load(f)
            for item, pos in items:
                print(item, pos)

    def on_actionSave(self):
        if not self.loaded_case:
            self.on_actionSaveAs()
            return

        with open('case.poi', 'wb') as f:
            items = [(item.block, (item.pos().x(), item.pos().y())) for item in self.graphics_view.scene().blockGraphicsItems()]
            pickle.dump(items, f)

    def on_actionSaveAs(self):
        self.loaded_case = 'test.poi'
        self.on_actionSave()

    def change_params(self, item):
        if item is self.solver_params:
            if self.main_tab_widget.widget(1):
                self.main_tab_widget.removeTab(1)
            self.main_tab_widget.addTab(self.solver_params_widget, 'Solver Parameters')
            self.main_tab_widget.setCurrentIndex(1)
        elif item is self.fluid_params:
            if self.main_tab_widget.widget(1):
                self.main_tab_widget.removeTab(1)
            self.main_tab_widget.addTab(self.fluid_params_widget, 'Fluid Parameters')
            self.main_tab_widget.setCurrentIndex(1)

    def change_connector_type(self, type):
        if type == 'Linear Resistance Connector':
            self.ConnectorType = LinearResistanceConnector
        elif type == 'Proctor and Gamble Connector':
            self.ConnectorType = ProctorAndGambleConnector
        else:
            raise ValueError('Unrecognized connector type "{}".'.format(type))

    def run_sim(self):
        blocks = self.graphics_view.scene().blocks()

        if blocks:
            system = IncompressibleSystem(blocks)
            system.solve(verbose=1)
        else:
            print('Scene is empty.')

    def run_optimizer(self):
        pass