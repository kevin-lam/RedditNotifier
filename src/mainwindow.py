from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic

class MainWindow(QtWidgets.QMainWindow):
  MAINWINDOW_UI_FILE = 'ui/main.ui'

  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)

  def display(self):
    uic.loadUi(self.MAINWINDOW_UI_FILE, self)
    self.show()

