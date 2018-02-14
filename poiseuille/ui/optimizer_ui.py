from PyQt5 import QtWidgets

import poiseuille.optimizers as opt
from poiseuille.components import procter_and_gamble

class OptimizerUi(QtWidgets.QWidget):
    def __init__(self, parent=None, scene=None):
        super().__init__(parent=parent)

        self.scene = scene

        self.setLayout(QtWidgets.QVBoxLayout())

        obj_box = QtWidgets.QGroupBox('Objectives')
        con_box = QtWidgets.QGroupBox('Constraints')

        self.objective_form = QtWidgets.QFormLayout()
        self.constraint_form = QtWidgets.QFormLayout()

        obj_box.setLayout(self.objective_form)
        con_box.setLayout(self.constraint_form)

        self.layout().addWidget(obj_box)
        self.layout().addWidget(con_box)

        self.block_check_box = {}
        self.block_enabled = {}

    def update_forms(self):
        fans = self.scene.blocks_of_type(procter_and_gamble.Fan)
        resistors = self.scene.blocks_of_type(procter_and_gamble.ResistorValve)

        for block in set(self.block_check_box.keys()):
            if block not in fans and block not in resistors:
                del self.block_check_box[block]
                del self.block_enabled[block]
            else:
                print(self.block_check_box[block].isChecked())
                self.block_enabled[block] = self.block_check_box[block].isChecked()

        for _ in range(self.objective_form.count()):
            self.objective_form.removeRow(0)

        for _ in range(self.constraint_form.count()):
            self.constraint_form.removeRow(0)

        for fan in sorted(fans, key=lambda f: f.name):
            check_box = QtWidgets.QCheckBox()
            check_box.setChecked(self.block_enabled.get(fan, False))

            self.block_check_box[fan] = check_box
            self.objective_form.addRow(QtWidgets.QLabel('{} --> objective enabled: '.format(fan.name)), check_box)

        for resistor in sorted(resistors, key=lambda r: r.name):
            check_box = QtWidgets.QCheckBox()
            check_box.setChecked(self.block_enabled.get(resistor, False))

            self.block_check_box[resistor] = check_box
            self.constraint_form.addRow(QtWidgets.QLabel('{} --> constraint enabled: '.format(resistor.name)), check_box)

    def solve(self):
        pass