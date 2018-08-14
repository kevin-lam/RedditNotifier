import sys

sys.path.append('..')

from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5 import QtCore
import sys

sys.path.append('..')

from PyQt5 import QtWidgets
from PyQt5 import uic

from widget import Widget
from dialog import EditEmailDialog, CreateNotificationDialog
from inputfile import UiFile


class MainWindow(QtWidgets.QMainWindow, Widget):

  def __init__(self):
    super(MainWindow, self).__init__()

#  def setup_ui_with_file(self, ui_file):
#    self.display(ui_file)

  def init(self):
    self.connect_buttons_to_actions()

#  def display(self, ui_file):
#    super(MainWindow, self).display(ui_file, self)

  def connect_buttons_to_actions(self):
    self.edit_email_button.clicked.connect(self.open_email_edit_dialog)
    self.new_notification_button.clicked.connect(self.open_create_notification_dialog)

  def open_email_edit_dialog(self):
    edit_email_dialog = EditEmailDialog()
    edit_email_dialog.setup(UiFile.EDIT_EMAIL_DIALOG)

  def open_create_notification_dialog(self):
    create_notification_dialog = CreateNotificationDialog()
    create_notification_dialog.setup(UiFile.CREATE_NOTIFICATION_DIALOG)
