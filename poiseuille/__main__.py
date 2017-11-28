import sys
from PyQt5.QtWidgets import QApplication
from poiseuille.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()