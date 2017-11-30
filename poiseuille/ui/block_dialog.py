from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLabel, QDoubleSpinBox, QFormLayout

class BlockDialog(QDialog):
    def __init__(self, block):
        super(BlockDialog, self).__init__()
        uic.loadUi('designer/blockdialog.ui', self)

        self.block = block
        self.property_dict = {}

        self.setWindowTitle('{}: {}'.format(self.block.type(), self.block.name))

        property_layout = self.property_box.layout()
        solution_layout = self.solution_box.layout()

        for key, value in self.block.properties().items():
            spin_box = QDoubleSpinBox()
            spin_box.setValue(value)
            spin_box.setDecimals(2)
            spin_box.setRange(-100., 100.)
            spin_box.setAccelerated(True)

            property_layout.addRow(QLabel(key), spin_box)
            self.property_dict[key] = spin_box

        for key, value in self.block.solution().items():
            solution_layout.addWidget(QLabel('{} = {}'.format(key, value)))

    def properties(self):
        return {
            key: value.value() for key, value in self.property_dict.items()
        }
