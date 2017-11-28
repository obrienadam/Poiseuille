from PyQt5 import QtWidgets, uic

class BlockDialog(QtWidgets.QDialog):
    def __init__(self, block):
        super(BlockDialog, self).__init__()
        uic.loadUi('designer/blockdialog.ui', self)

        self.block = block

        self.setWindowTitle('{}: {}'.format(self.block.type(), self.block.name))

        property_layout = self.property_box.layout()
        solution_layout = self.solution_box.layout()

        for key, value in self.block.properties().items():
            property_layout.addRow(QtWidgets.QLabel(key), QtWidgets.QDoubleSpinBox())

        for key, value in self.block.solution().items():
            solution_layout.addWidget(QtWidgets.QLabel('{} = {}'.format(key, value)))

    def accept(self):
        print('fad')

