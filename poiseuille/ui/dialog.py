from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLabel, QDoubleSpinBox, QFormLayout

class BlockDialog(QDialog):
    def __init__(self, block):
        super().__init__()
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

class ConnectorDialog(QDialog):
    def __init__(self, connector):
        super().__init__()
        uic.loadUi('designer/blockdialog.ui', self)

        self.connector = connector
        self.property_dict = {}

        self.setWindowTitle('{}: {}'.format(self.connector.type(), self.connector.name))

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

class VariableDefinitionDialog(QDialog):
    def __init__(self, blocks):
        super().__init__()
        uic.loadUi('designer/variable_definition.ui', self)
        self.options = []

        for block in blocks:
            self.options.append({
                'block': block,
                'properties': [prop for prop in block.properties()],
                'solution': [sol for sol in block.solution()]
            })

            self.block_combo_box.addItem(block.name)

        self.property_radio_button.toggled.connect(self.set_variable_type)
        self.block_combo_box.currentIndexChanged.connect(self.change_block)

        if not self.options:
            self.block_combo_box.setDisabled(True)
            self.property_combo_box.setDisabled(True)
        else:
            self.change_block(0)

    def set_variable_type(self, is_property_type):
        self.property_combo_box.clear()
        index = self.block_combo_box.currentIndex()
        if index >= 0:
            if is_property_type:
                self.property_combo_box.addItems(self.options[index]['properties'])
            else:
                self.property_combo_box.addItems(self.options[index]['solution'])

        self.property_combo_box.setDisabled(self.property_combo_box.count() == 0)

    def change_block(self, index):
        self.property_combo_box.clear()
        self.set_variable_type(self.property_radio_button.isChecked())

    def get_new_variable(self):
        if self.block_combo_box.count() and self.property_combo_box.count() and self.variable_name_line_edit.text():
            opt = self.options[self.block_combo_box.currentIndex()]
            block = opt['block']
            prop = opt['properties'][self.property_combo_box.currentIndex()]
            name = self.variable_name_line_edit.text()
            return block, prop, name
