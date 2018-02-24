from PyQt5 import QtWidgets

import poiseuille.systems as sys
import poiseuille.optimizers as opt
from poiseuille.components import procter_and_gamble

class OptimizerUi(QtWidgets.QWidget):
    def __init__(self, parent=None, scene=None):
        super().__init__(parent=parent)

        self.scene = scene
        self.setLayout(QtWidgets.QHBoxLayout())

        self.target_block_combo_box = QtWidgets.QComboBox()
        self.target_block_combo_box.addItems(['Fan'])
        self.target_property_combo_box = QtWidgets.QComboBox()
        self.target_property_combo_box.addItems(['Pressure differential'])
        self.objective_function_combo_box = QtWidgets.QComboBox()
        self.objective_function_combo_box.addItems(['Minimize sum of squares', 'Minimize sum of absolute values'])


        self.form = QtWidgets.QFormLayout()
        self.form.addRow(QtWidgets.QLabel('Objective target block: '), self.target_block_combo_box)
        self.form.addRow(QtWidgets.QLabel('Objective target property: '), self.target_property_combo_box)
        self.form.addRow(QtWidgets.QLabel('Objective function: '), self.objective_function_combo_box)

        self.layout().addLayout(self.form)

    def init(self, **kwargs):
        pass

    def parameters(self):
        return {}

    def solve(self):
        self.system = sys.IncompressibleSystem(blocks=self.scene.blocks())
        self.optimizer = opt.Optimizer(system=self.system)
        self.optimizer.init_property_objective_function(
            self.scene.blocks_of_type(self.target_block_combo_box.currentText()),
            self.target_property_combo_box.currentText()
        )

        for block in self.scene.blocks():
            for name, constr in block.constraints.items():
                if constr['active']:
                    if constr['dependent']:
                        self.optimizer.add_solution_constraint(block, name, constr['type'], constr['value'])
                    else:
                        self.optimizer.add_property_constraint(block, name, constr['type'], constr['value'])

                    for prop, data in block.properties().items():
                        if data['range'][0] != float('-inf'):
                            self.optimizer.add_property_constraint(block, prop, 'ineq', data['range'][0])

        for block in self.scene.blocks():
            if block in self.optimizer.objective_func.blocks:
                for prop, data in block.properties().items():
                    if data['range'][0] != float('-inf'):
                        self.optimizer.add_property_constraint(block, prop, 'ineq', data['range'][0])

        x0 = []
        for fan in self.scene.blocks_of_type(procter_and_gamble.Fan):
            x0.append(fan.dp)

        for r in self.scene.blocks_of_type(procter_and_gamble.ResistorValve):
            x0.append(r.r)

        self.optimizer.optimize(x0, maxiter=1000, verbose=1)