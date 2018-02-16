from PyQt5 import QtWidgets

import poiseuille.systems as sys
from poiseuille.systems import Status


class SystemUi(QtWidgets.QWidget):
    def __init__(self, parent=None, scene=None):
        super().__init__(parent=parent)

        self.scene = scene

        self.setLayout(QtWidgets.QFormLayout())

        self.system_status_label = QtWidgets.QLabel('Unsolved')

        self.solver_combo_box = QtWidgets.QComboBox()
        self.solver_combo_box.addItem('BiCGSTAB')
        self.solver_combo_box.addItem('GMRES')
        self.solver_combo_box.addItem('LGMRES')

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

        self.verbose_check_box = QtWidgets.QCheckBox()

        # All params that are initialized
        self.layout().addRow(QtWidgets.QLabel('System status: '), self.system_status_label)
        self.layout().addRow(QtWidgets.QLabel('Solver: '), self.solver_combo_box)
        self.layout().addRow(QtWidgets.QLabel('Max iters: '), self.max_iters_spin_box)
        self.layout().addRow(QtWidgets.QLabel('Tolerance: '), self.tol_spin_box)
        self.layout().addRow(QtWidgets.QLabel('Verbose console output: '), self.verbose_check_box)

        self.set_sytem_type('Incompressible')

    def init(self, **kwargs):
        self.system_status_label.setText(kwargs.get('System status', self.system_status_label.text()))
        self.solver_combo_box.setCurrentText(kwargs.get('Solver', self.solver_combo_box.currentText()))
        self.max_iters_spin_box.setValue(kwargs.get('Max iters', self.max_iters_spin_box.value()))
        self.tol_spin_box.setValue(kwargs.get('Tolerance', self.tol_spin_box.value()))

    def parameters(self):
        return {
            'System status': self.system_status_label.text(),
            'Solver': self.solver_combo_box.currentText(),
            'Max iters': self.max_iters_spin_box.value(),
            'Tolerance': self.tol_spin_box.value()
        }

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
            verbose=self.verbose_check_box.isChecked()
        )

        if self.system.status == Status.SOLVED:
            self.system_status_label.setText('Solved')
        elif self.system.status == Status.INVALID_SYSTEM_STATE:
            self.system_status_label.setText('Invalid state')
        elif self.system.status == Status.NO_CONVERGENCE:
            self.system_status_label.setText('Failed to converge')
