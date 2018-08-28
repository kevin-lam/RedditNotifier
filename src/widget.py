from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class Widget(QWidget):

  def __init__(self, ui_file, base_instance):
    super(Widget, self).__init__()
    uic.loadUi(ui_file, self)
    self.setup_signals()
