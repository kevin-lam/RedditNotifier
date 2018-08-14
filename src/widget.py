from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class Widget(QWidget):

  def __init__(self):
    super(Widget, self).__init__()

  def setup(self, ui_file, base_class=None):
    base_class = self if base_class is None else base_class
    self.display(ui_file, base_class)
    self.init()

  def display(self, ui_file, base_class):
    uic.loadUi(ui_file, base_class)
    self.show_ui(base_class)

  def show_ui(self, instance):
    instance.show()
