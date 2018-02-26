from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLabel, QDoubleSpinBox, QHBoxLayout, QCheckBox


class Dialog(QDialog):
    def __init__(self, component):
        super().__init__()

        uic.loadUi('designer/component_dialog.ui', self)

        self.component = component
        self.property_dict = {}
        self.constraint_dict = {}

        self.setWindowTitle('{}: {}'.format(component.TYPE, component.name))

        for key, value in component.properties().items():
            spin_box = self.get_spin_box(value=value['value'], range=value['range'], decimals=value.get('precision', 2))

            if key in component.UNITS:
                self.property_box.layout().addRow(QLabel('{} ({})'.format(key, component.UNITS[key])), spin_box)
            else:
                self.property_box.layout().addRow(QLabel(key), spin_box)

            self.property_dict[key] = spin_box

        for name, constr in component.constraints.items():
            type = constr['type']
            value = constr['value']

            range = float('-inf'), float('inf')

            if name in self.component.properties():
                range = self.component.properties()[name]['range']

            spin_box = self.get_spin_box(value=value, range=range, decimals=8)
            check_box = self.get_check_box(constr['active'], 'Enabled', spin_box)

            field = QHBoxLayout()
            field.addWidget(spin_box)
            field.addWidget(check_box)

            self.constraint_dict[name] = {
                'value': spin_box,
                'active': check_box
            }

            self.optimizer_constraint_box.layout().addRow(QLabel('{} {} '.format(name, '>' if type == 'ineq' else '=')),
                                                          field)

        for key, value in component.solution().items():
            disp = '{:.2f}'.format(value) if abs(value) >= 0.1 or value == 0. else '{:.2e}'.format(value)
            self.solution_box.layout().addWidget(
                QLabel('{} = {} {}'.format(key, disp, component.UNITS.get(key, '')))
            )

        for node in component.nodes:
            disp = '{:.2f}'.format(node.p) if abs(node.p) >= 0.1 or node.p == 0. else '{:.2e}'.format(node.p)
            self.node_pressure_box.layout().addWidget(
                QLabel('{} (id={}) = {} {}'.format(node.TYPE, node.id, disp, component.UNITS['Pressure']))
            )

        for box in self.solution_box, self.optimizer_constraint_box:
            if box.layout().isEmpty():
                box.hide()

    def properties(self):
        return {
            key: value.value() for key, value in self.property_dict.items()
        }

    def constraints(self):
        return {
            name: {
                'value': constr['value'].value(),
                'active': constr['active'].isChecked()
            } for name, constr in self.constraint_dict.items()
        }

    def get_spin_box(self, value=None, range=None, decimals=14):
        spin_box = QDoubleSpinBox()
        spin_box.setRange(*range)
        spin_box.setDecimals(decimals)
        spin_box.setValue(value)
        spin_box.setSingleStep(min((range[1] - range[0]) / 100., 1))
        spin_box.setAccelerated(True)
        return spin_box

    def get_check_box(self, checked=False, text=None, connected_widget=None):
        check_box = QCheckBox()
        check_box.setChecked(checked)
        check_box.setText(text)

        if connected_widget:
            check_box.toggled.connect(connected_widget.setEnabled)
            connected_widget.setEnabled(check_box.isChecked())

        return check_box
