from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from widget import Widget

class ModalDialog(QDialog, Widget):
  def show_ui(self, instance):
    instance.exec_()

  def close_dialog_return_valid(self):
    self.accept()

class EditEmailDialog(ModalDialog, Widget):
  def __init__(self):
    super(EditEmailDialog, self).__init__()

  def init(self):
    self.connect_buttons_to_actions()
    self._hide_invalid_email()

  def connect_buttons_to_actions(self):
    self.confirm_button.clicked.connect(self.validate_email)

  def validate_email(self):
    email = self._get_email()
    if self._email_is_valid(email):
      self._hide_invalid_email()
      self.close_dialog_return_valid()
    else:
      self._display_invalid_email()

  def _get_email(self):
    pass

  def _email_is_valid(self, email):
    #self.email_validator.is_email_valid(email)
    pass

  def _hide_invalid_email(self):
    self.invalid_email_label.hide()

  def _display_invalid_email(self):
    self.invalid_email_label.show()



class CreateNotificationDialog(ModalDialog, Widget):
  def __init__(self):
    super(CreateNotificationDialog, self).__init__()
