from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLabel, QDoubleSpinBox, QFormLayout

class BlockDialog(QDialog):
    def __init__(self, block):
        super().__init__()
        uic.loadUi('designer/blockdialog.ui', self)

        self.block = block
        self.property_dict = {}

        self.setWindowTitle('{}: {}'.format(self.block.TYPE, self.block.name))

        property_layout = self.property_box.layout()
        solution_layout = self.solution_box.layout()
        node_pressure_layout = self.node_pressure_box.layout()

        for key, value in self.block.properties().items():
            range = block.property_ranges().get(key, (None, None))
            range = range[0] if range[0] is not None else -float('inf'), range[1] if range[1] is not None else float('inf')

            spin_box = QDoubleSpinBox()
            spin_box.setRange(*range)
            spin_box.setDecimals(14)
            spin_box.setValue(value)
            spin_box.setAccelerated(True)

            if key in block.UNITS:
                property_layout.addRow(QLabel('{} ({})'.format(key, block.UNITS[key])), spin_box)
            else:
                property_layout.addRow(QLabel(key), spin_box)

            self.property_dict[key] = spin_box

        for key, value in self.block.solution().items():
            solution_layout.addWidget(QLabel('{} = {}'.format(key, value)))

        for node in self.block.nodes:
            node_pressure_layout.addWidget(QLabel('{} ({}) = {}'.format(node.id, node.TYPE, node.p)))

    def properties(self):
        return {
            key: value.value() for key, value in self.property_dict.items()
        }

class ConnectorDialog(QDialog):
    def __init__(self, connector):
        super().__init__()
        uic.loadUi('designer/blockdialog.ui', self)

        self.connector = connector
        self.property_dict = {}

        self.setWindowTitle('{}: {}'.format(self.connector.TYPE, self.connector.name))

        property_layout = self.property_box.layout()
        solution_layout = self.solution_box.layout()

        for key, value in self.connector.properties().items():
            spin_box = QDoubleSpinBox()
            spin_box.setValue(value)
            spin_box.setDecimals(2)
            spin_box.setRange(-100., 100.)
            spin_box.setAccelerated(True)

            property_layout.addRow(QLabel(key), spin_box)
            self.property_dict[key] = spin_box

        for key, value in self.connector.solution().items():
            solution_layout.addWidget(QLabel('{} = {}'.format(key, value)))

    def properties(self):
        return {
            key: value.value() for key, value in self.property_dict.items()
        }
