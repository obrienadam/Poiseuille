import pickle

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QFileDialog, QGraphicsView
from PyQt5 import uic

from .graphics_scene import GraphicsScene
from ..ui import procter_and_gamble
from .palette import BlockPalette

from .system_ui import SystemUi
from .optimizer_ui import OptimizerUi

from poiseuille.systems.system import IncompressibleSystem
from poiseuille.optimizers.optimizers import Optimizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(uifile='designer/mainwindow.ui', baseinstance=self)

        self.scene = GraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Main classes
        self.init_parameters_tree()
        self.init_palettes()
        self.init_actions()
        self.loaded_case = None
        self.saved = True
        self.showMaximized()

    def init_parameters_tree(self):
        self.system_params_tree_item = self.parameters_tree.topLevelItem(0).child(0)
        self.optimizer_params_tree_item = self.parameters_tree.topLevelItem(0).child(1)
        self.block_list_tree_item = self.parameters_tree.topLevelItem(0).child(2)
        self.connector_list_tree_item = self.parameters_tree.topLevelItem(0).child(3)

        self.system_params = SystemUi(scene=self.scene)
        self.optimizer_params = OptimizerUi(scene=self.scene)

    def init_palettes(self):
        self.environment_palette = BlockPalette()
        self.power_palette = BlockPalette()
        self.flow_control_palette = BlockPalette()
        self.jointers_splitters_palette = BlockPalette()

        self.palette_tabs.addTab(self.environment_palette, 'Environment')
        self.palette_tabs.addTab(self.power_palette, 'Power')
        self.palette_tabs.addTab(self.flow_control_palette, 'Flow Control')
        self.palette_tabs.addTab(self.jointers_splitters_palette, 'Joiners/Splitters')

        self.environment_palette.add_block_type(procter_and_gamble.PressureReservoirGraphicsItem)
        self.power_palette.add_block_type(procter_and_gamble.FanGraphicsItem)
        self.flow_control_palette.add_block_type(procter_and_gamble.ResistorValveGraphicsItem)
        self.flow_control_palette.add_block_type(procter_and_gamble.PressureValveGraphicsItem)
        self.flow_control_palette.add_block_type(procter_and_gamble.FlowRegulatorGraphicsItem)
        self.jointers_splitters_palette.add_block_type(procter_and_gamble.JoinerGraphicsItem)

    def init_actions(self):
        # Parameter tree
        self.parameters_tree.itemDoubleClicked.connect(self.change_params)

        # Solver parameters
        #self.resistance_combo_box.currentTextChanged.connect(self.change_resistance_type)

        # Optimizer parameters
        #self.new_variable_push_button.pressed.connect(self.create_optimizer_variable)

        # Toolbar
        self.toolBar.actions()[0].triggered.connect(self.run_sim)
        self.toolBar.actions()[2].triggered.connect(self.run_optimizer)

        # Menu
        actions = self.menuFile.actions()
        actions[0].triggered.connect(self.on_actionNew)
        actions[1].triggered.connect(self.on_actionOpen)
        actions[2].triggered.connect(self.on_actionSave)
        actions[3].triggered.connect(self.on_actionSaveAs)

    def on_actionNew(self):
        if not self.saved:
            pass



    def on_actionOpen(self):
        if not self.saved:
            pass

        dialog = QFileDialog()

        if dialog.exec():
            with open(dialog.selectedFiles()[0], 'rb') as f:
                try:
                    data = pickle.load(f)
                    self.system_params.init(**data['solver_params'])
                    self.optimizer_params.init(**data['optimizer_params'])
                    self.scene.load(data['blocks'], data['positions'])
                    self.loaded_case = f.name
                except pickle.UnpicklingError as e:
                    print('Error loading file "{}". File may be corrupted.'.format(f.name))

    def on_actionSave(self):
        if not self.loaded_case:
            self.on_actionSaveAs()

        if self.loaded_case:
            with open(self.loaded_case, 'wb') as f:
                data = {
                    'blocks': self.scene.blocks(),
                    'positions': self.scene.block_positions(),
                    'solver_params': self.system_params.parameters(),
                    'optimizer_params': self.optimizer_params.parameters(),
                }

                pickle.dump(data, f)

    def on_actionSaveAs(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptSave)

        if dialog.exec():
            with open(dialog.selectedFiles()[0], 'wb') as f:
                self.loaded_case = f.name

    def change_params(self, item):
        if self.main_tab_widget.widget(1):
            self.main_tab_widget.removeTab(1)

        if item is self.system_params_tree_item:
            self.main_tab_widget.addTab(self.system_params, 'System Parameters')
        elif item is self.optimizer_params_tree_item:
            self.main_tab_widget.addTab(self.optimizer_params, 'Optimizer Parameters')

        self.main_tab_widget.setCurrentIndex(1)

    def run_sim(self):
        self.system_params.solve()

    def run_optimizer(self):
        self.optimizer_params.solve()