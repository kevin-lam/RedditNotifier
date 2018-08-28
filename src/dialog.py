from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog
from widget import Widget
from scheduler import Task, TaskTrigger, TaskName
from user import User
from reddit import RedditQuery, RedditQueryListing

class TwoButtonModalDialog(QDialog, Widget):
  def __init__(self, ui_file, base_instance):
    super(TwoButtonModalDialog, self).__init__(ui_file, base_instance)
    self.setup_ui()

  def return_valid(self):
    self.accept()

  def return_failure(self):
    self.reject()


class UserDialog(TwoButtonModalDialog):

  confirm_clicked = pyqtSignal()

  def __init__(self, ui_file):
    super(UserDialog, self).__init__(ui_file, self)

  def setup_signals(self):
    self.confirm_button.clicked.connect(self._confirm_clicked)
    self.cancel_button.clicked.connect(self._cancel_clicked)

  def setup_ui(self):
    self.hide_invalid_email()

  def _confirm_clicked(self):
    self.confirm_clicked.emit()
    
  def _cancel_clicked(self):
    self.return_failure()

  def hide_invalid_email(self):
    self.invalid_email_label.hide()

  def show_invalid_email(self):
    self.invalid_email_label.show()

  def set_email(self, email):
    self.email_line_edit.setText(email)

  def get_email(self):
    return self.email_line_edit.text()


class UserDialogPresenter:

  def __init__(self, user_dialog_view, user_dialog_model):
    self.user_dialog_view = user_dialog_view
    self.user_dialog_model = user_dialog_model
    self.set_existing_email()

  def set_existing_email(self):
    user = self.user_dialog_model.get_user()
    self.user_dialog_view.set_email(user.email)

  def validate_user_info(self):
    user = self._create_user_from_input()
    if self.user_dialog_model.user_info_valid(user):
      self.user_dialog_model.save_user(user)
      self.user_dialog_view.hide_invalid_email()
      self.user_dialog_view.return_valid()
    else:
      self.user_dialog_view.show_invalid_email()

  def _create_user_from_input(self):
    email = self.user_dialog_view.get_email()
    return User(email)

class UserDialogModel:

  def __init__(self, scheduler, user_storage, user_validator):
    self.scheduler = scheduler
    self.user_storage = user_storage
    self.user_validator = user_validator

  def user_info_valid(self, user):
    return self.user_validator.user_info_valid(user)

  def get_user(self):
    return self.user_storage.read_all(default=User())

  def save_user(self, user):
    self.scheduler.schedule_task(Task(lambda: self.user_storage.overwrite(user), trigger=TaskTrigger.ONE_OFF,
                                      name=TaskName.OVERWRITE_USER))


class QueryDialog(TwoButtonModalDialog):

  confirm_clicked = pyqtSignal()

  def __init__(self, ui_file):
    super(QueryDialog, self).__init__(ui_file, self)

  def setup_ui(self):
    self.hide_invalid_subreddit()

  def setup_signals(self):
    self.confirm_button.clicked.connect(self._confirm_clicked)
    self.cancel_button.clicked.connect(self._cancel_clicked)

  def hide_invalid_subreddit(self):
    self.invalid_subreddit_label.hide()

  def show_invalid_subreddit(self):
    self.invalid_subreddit_label.show()

  def _confirm_clicked(self):
    self.confirm_clicked.emit()

  def _cancel_clicked(self):
    self.return_failure()

  def get_subreddit(self):
    return self.subreddit_line_edit.text()

  def get_keyword(self):
    return self.search_line_edit.text()

class QueryDialogPresenter:

  def __init__(self, query_dialog_view, query_dialog_model):
    self.query_dialog_view = query_dialog_view
    self.query_dialog_model = query_dialog_model

  def validate_subreddit(self):
    keyword = self.query_dialog_view.get_keyword()
    subreddit = self.query_dialog_view.get_subreddit()
    if self.query_dialog_model.subreddit_valid(subreddit):
      self.query_dialog_model.save_query(RedditQuery(keyword, subreddit))
      self.query_dialog_view.hide_invalid_subreddit()
      self.query_dialog_view.return_valid()
    else:
      self.query_dialog_view.show_invalid_subreddit()


class QueryDialogModel:
  def __init__(self, scheduler, query_storage, reddit):
    self.scheduler = scheduler
    self.query_storage = query_storage
    self.reddit = reddit

  def subreddit_valid(self, subreddit):
    return self.reddit.subreddit_exists(subreddit)

  def save_query(self, query):
    self.scheduler.schedule_task(Task(lambda: self.query_storage.append(query, default=RedditQueryListing()),
                                 trigger=TaskTrigger.ONE_OFF, name=TaskName.APPEND_QUERY, id=query.id))
