import pickle

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QFileDialog
from PyQt5 import uic

from .graphics_scene import GraphicsScene
from ..ui import procter_and_gamble
from .palette import BlockPaletteItem
from .dialog import VariableDefinitionDialog

from poiseuille.systems.system import IncompressibleSystem
from poiseuille.optimizers.optimizers import Optimizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(uifile='designer/mainwindow.ui', baseinstance=self)

        view = self.graphics_view
        scene = GraphicsScene(view)
        view.setScene(scene)

        # Main classes
        self.optimizer = Optimizer()

        self.init_parameters_tree()
        self.init_palettes()
        self.init_actions()
        self.loaded_case = None
        self.saved = True
        self.show()

    def init_parameters_tree(self):
        pass

    def init_palettes(self):
        self.palette_env.setLayout(QHBoxLayout())
        self.palette_power.setLayout(QHBoxLayout())
        self.palette_valves.setLayout(QHBoxLayout())

        self.palette_env.layout().addWidget(BlockPaletteItem(block=procter_and_gamble.PressureReservoirGraphicsItem))
        self.palette_power.layout().addWidget(BlockPaletteItem(block=procter_and_gamble.FanGraphicsItem))
        self.palette_power.layout().addWidget(BlockPaletteItem(block=procter_and_gamble.ConstDeliveryFanGraphicsItem))
        self.palette_valves.layout().addWidget(BlockPaletteItem(block=procter_and_gamble.RestrictorValveGraphicsItem))
        self.palette_valves.layout().addWidget(BlockPaletteItem(block=procter_and_gamble.JoinerGraphicsItem))

    def init_actions(self):
        self.solver_params = self.parameters_tree.topLevelItem(0).child(0)
        self.fluid_params = self.parameters_tree.topLevelItem(0).child(1)
        self.optimizer_params = self.parameters_tree.topLevelItem(0).child(2)
        self.block_list = self.parameters_tree.topLevelItem(0).child(3)
        self.connector_list = self.parameters_tree.topLevelItem(0).child(4)
        self.solver_params_widget = self.main_tab_widget.widget(1)
        self.fluid_params_widget = self.main_tab_widget.widget(2)
        self.optimizer_params_widget = self.main_tab_widget.widget(3)

        self.main_tab_widget.removeTab(1)
        self.main_tab_widget.removeTab(1)

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
                    self.graphics_view.scene().load(data['blocks'], data['positions'])
                    self.loaded_case = f.name
                except pickle.UnpicklingError as e:
                    print('Error loading file "{}". File may be corrupted.'.format(f.name))

    def on_actionSave(self):
        if not self.loaded_case:
            self.on_actionSaveAs()

        with open(self.loaded_case, 'wb') as f:
            data = {
                'blocks': self.graphics_view.scene().blocks(),
                'positions': [(item.scenePos().x(), item.scenePos().y()) for item in
                              self.graphics_view.scene().blockGraphicsItems()],
                'solver_params': {},
                'optimizer_params': {},
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

        if item is self.solver_params:
            self.main_tab_widget.addTab(self.solver_params_widget, 'Solver Parameters')
            self.main_tab_widget.setCurrentIndex(1)
        elif item is self.fluid_params:
            self.main_tab_widget.addTab(self.fluid_params_widget, 'Fluid Parameters')
            self.main_tab_widget.setCurrentIndex(1)
        elif item is self.optimizer_params:
            self.main_tab_widget.addTab(self.optimizer_params_widget, 'Optimizer Parameters')
            self.main_tab_widget.setCurrentIndex(1)

    def run_sim(self):
        blocks = self.graphics_view.scene().blocks()

        if blocks:
            system = IncompressibleSystem(blocks)
            system.solve(maxiter=5000, method='lgmres', verbose=1)
        else:
            print('Scene is empty.')

    def run_optimizer(self):
        print('Running optimizer!')

    def create_optimizer_variable(self):
        dialog = VariableDefinitionDialog(blocks=self.graphics_view.scene().blocks())

        if dialog.exec() == dialog.Accepted:
            var = dialog.get_new_variable()
            if var:
                self.optimizer.add_variable(*var)