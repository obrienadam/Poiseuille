from PyQt5 import QtWidgets

import poiseuille.systems as sys


class SystemUi(QtWidgets.QWidget):
    def __init__(self, parent=None, scene=None):
        super().__init__(parent=parent)

        self.scene = scene

        self.setLayout(QtWidgets.QFormLayout())

        self.solver_combo_box = QtWidgets.QComboBox()
        self.solver_combo_box.addItem('LGMRES')
        self.solver_combo_box.addItem('GMRES')
        self.solver_combo_box.addItem('BiCGSTAB')

        self.max_iters_spin_box = QtWidgets.QSpinBox()
        self.max_iters_spin_box.setMinimum(1)
        self.max_iters_spin_box.setMaximum(1e6)
        self.max_iters_spin_box.setValue(5000)

        self.tol_spin_box = QtWidgets.QDoubleSpinBox()
        self.tol_spin_box.setMinimum(0.)
        self.tol_spin_box.setMaximum(1.)
        self.tol_spin_box.setAccelerated(True)
        self.tol_spin_box.setDecimals(15)
        self.tol_spin_box.setSingleStep(1e-5)
        self.tol_spin_box.setValue(1e-4)

        self.layout().addRow(QtWidgets.QLabel('Solver: '), self.solver_combo_box)
        self.layout().addRow(QtWidgets.QLabel('Max iters: '), self.max_iters_spin_box)
        self.layout().addRow(QtWidgets.QLabel('Tolerance: '), self.tol_spin_box)

        self.set_sytem_type('Incompressible')

    def set_sytem_type(self, sytem_type):
        if sytem_type == 'Incompressible':
            self.system = sys.IncompressibleSystem()
        else:
            self.system = None

    def update_system(self, blocks):
        pass

    def solve(self):
        self.system = sys.IncompressibleSystem(blocks=self.scene.blocks())

        self.system.solve(
            maxiter=self.max_iters_spin_box.value(),
            toler=self.tol_spin_box.value(),
            method=self.solver_combo_box.currentText().lower(),
            verbose=1
        )
