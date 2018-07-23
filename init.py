from PyQt5 import QtWidgets

from src.MainWindow import MainWindow

import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
