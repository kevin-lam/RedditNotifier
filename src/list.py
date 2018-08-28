import sys

sys.path.append('..')

from PyQt5.QtCore import pyqtSignal
from widget import Widget
from scheduler import TaskState
from inputfile import UiFile

class QueryListingEntry(Widget):

  pause_clicked = pyqtSignal(object)
  resume_clicked = pyqtSignal(object)
  stop_clicked = pyqtSignal(object)

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
    self.hide_resume_button()

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
    self.total_post_count = total_post_count

  def set_id(self, id):
    self.id = id

  def set_state(self, state):
    if state is TaskState.RESUMED:
      self.hide_pause_button()
    elif state is TaskState.PAUSED:
      self.hide_resume_button()

  def hide_resume_button(self):
    self.resume_button.hide()
    self.pause_button.show()

  def hide_pause_button(self):
    self.pause_button.hide()
    self.resume_button.show()

  def _pause_clicked(self):
    self.pause_clicked.emit(self)

  def _resume_clicked(self):
    self.resume_clicked.emit(self)

  def _stop_clicked(self):
    self.stop_clicked.emit(self)
