import sys

sys.path.append('..')

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QListWidgetItem
from widget import Widget
from scheduler import TaskState
from inputfile import UiFile

class QueryListingEntry(Widget):

  pause_clicked = pyqtSignal(object, object)
  resume_clicked = pyqtSignal(object, object)
  stop_clicked = pyqtSignal(object, object)

  def __init__(self, query):
    super(QueryListingEntry, self).__init__(UiFile.QUERYLISTING_ENTRY, self)
    self.query = query
    self.setup_ui()

  def setup_signals(self):
    self.pause_button.clicked.connect(self._pause_clicked)
    self.stop_button.clicked.connect(self._stop_clicked)
    self.resume_button.clicked.connect(self._resume_clicked)

  def setup_ui(self):
    self.set_query_values(self.query)

  def set_query_values(self, query):
    self.query = query
    self.set_keyword(query.keyword)
    self.set_subreddit(query.subreddit)
    self.set_post_count(query.total_post_count)
    self.set_id(query.id)
    self.set_state(query.state)

  def set_keyword(self, keyword):
    self.keyword_label.setText(keyword)

  def set_subreddit(self, subreddit):
    self.subreddit_label.setText(subreddit)

  def set_post_count(self, total_post_count):
    self.total_post_count_label.setText(str(total_post_count))

  def set_id(self, id):
    self.id = id

  def set_state(self, state):
    if state is TaskState.RESUMED:
      self.hide_resume_button()
    elif state is TaskState.PAUSED:
      self.hide_pause_button()

  def hide_resume_button(self):
    self.resume_button.hide()
    self.pause_button.show()

  def hide_pause_button(self):
    self.pause_button.hide()
    self.resume_button.show()

  def _pause_clicked(self):
    self.pause_clicked.emit(self, self.query)

  def _resume_clicked(self):
    self.resume_clicked.emit(self, self.query)

  def _stop_clicked(self):
    self.stop_clicked.emit(self, self.query)


class QueryListingItem(QListWidgetItem):
  def __init__(self, list, query):
    super(QueryListingItem, self).__init__(list)
    self.compare_by_query_value(query)

  def compare_by_query_value(self, query):
    self.setData(Qt.UserRole, query.subreddit)

  def __lt__(self, other):
    return self.data(Qt.UserRole) < other.data(Qt.UserRole)
