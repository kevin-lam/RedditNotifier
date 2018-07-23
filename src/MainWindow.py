from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi('ui/main.ui', self)
        self.show()

