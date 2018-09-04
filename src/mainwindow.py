import sys

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSize

sys.path.append('..')

from widget import Widget
from scheduler import Task, TaskTrigger, TaskName, TaskState, Time
from reddit import RedditQueryListing
from inputfile import UiFile
from list import QueryListingEntry, QueryListingItem
from electronicmail import RedditEmail
from user import User
from date import DateTime

class MainWindow(QtWidgets.QMainWindow, Widget):

  user_dialog_clicked = pyqtSignal()
  query_dialog_clicked = pyqtSignal()

  def __init__(self, ui_file):
    super(MainWindow, self).__init__(ui_file, self)

  def setup_signals(self):
    self.user_dialog_button.clicked.connect(self._on_user_dialog_clicked)
    self.query_dialog_button.clicked.connect(self._on_query_dialog_clicked)

  def _on_user_dialog_clicked(self):
    self.user_dialog_clicked.emit()

  def _on_query_dialog_clicked(self):
    self.query_dialog_clicked.emit()

  def enable_query_dialog_button(self):
    self.query_dialog_button.setEnabled(True)

  def set_query_count(self, count):
    self.notification_count_label.setText(str(count))
    notification_label_text = "Notification" if count <= 1 else "Notifications"
    self.notification_label.setText(notification_label_text)

  def get_query_count(self):
    return int(self.notification_count_label.text())

  def create_list_item(self, query):
    return QueryListingItem(self.notification_list, query)

  def create_entry(self, query):
    return QueryListingEntry(query)

  def add_listing_item_entry(self, item, entry):
    item.setSizeHint(entry.sizeHint())
    self.notification_list.addItem(item)
    self.notification_list.setItemWidget(item, entry)

  def update_entry(self, item, entry):
    self.notification_list.setItemWidget(item, entry)

  def remove_entry(self, item):
    self.notification_list.removeItemWidget(item)

class MainWindowPresenter:

  def __init__(self, main_window_view, main_window_model):
    self.main_window_view = main_window_view
    self.main_window_model = main_window_model
    self.id_to_item_map = {}
    self.when_user_ready()

  def when_user_ready(self):
    self.main_window_model.get_querylisting()

  def when_query_ready(self, id):
    self.main_window_model.get_query_by_id(id)

  def with_querylisting(self, querylisting):
    if not self.main_window_model.has_existing_queries():
      self._display(querylisting)
      self._query(querylisting)

  def with_query(self, query):
    querylisting = RedditQueryListing()
    querylisting.add(query)
    self._display(querylisting)
    self._query(querylisting)

  def _display(self, querylisting):
    if self.main_window_model.user_exist():
      self._create_querylisting_entry(querylisting)
      self.main_window_view.set_query_count(self.main_window_view.get_query_count() + querylisting.size())
      self.main_window_view.enable_query_dialog_button()

  def _query(self, querylisting):
    if self.main_window_model.user_exist():
      self.main_window_model.search_reddit(querylisting)

  def _create_querylisting_entry(self, querylisting):
    for id, query in querylisting.listing.items():
      item = self.main_window_view.create_list_item(query)
      entry = self.main_window_view.create_entry(query)
      self._map_id_to_item(id, item)
      self.setup_entry_signals(item, entry)
      self.main_window_view.add_listing_item_entry(item, entry)

  def _map_id_to_item(self, id, item):
    self.id_to_item_map[id] = item

  def _unmap_id_to_item(self, id):
    del self.id_to_item_map[id]

  def with_query_result(self, id, query_result):
    query = self.main_window_model.get_query_by_id_immediate(id)
    print query.keyword
    print query.subreddit
    print query.most_recent_post_date
    for post in query_result:
      print post.title
      print post.date
    query_result = self._trim_result(query, query_result)
    if query_result:
      query.total_post_count += len(query_result)
      self._update_entry(id, query)
      self.main_window_model.send_email_notification(query, query_result)

  def _trim_result(self, query, result):
    return [post for post in reversed(result) if self._post_is_new(query, post)]

  def _post_is_new(self, query, post):
    is_new = post.date > query.most_recent_post_date
    if is_new:
      query.most_recent_post_date = post.date
    return is_new

  def _update_entry(self, id, query):
    item = self.id_to_item_map[id]
    item.compare_by_query_value(query)
    entry = self.main_window_view.create_entry(query)
    self.setup_entry_signals(item, entry)
    self.main_window_model.update_query_task(id, query)
    self.main_window_model.update_storage(id, query)
    self.main_window_view.update_entry(item, entry)

  def _remove_entry(self, id, query):
    item = self.id_to_item_map[id]
    item.compare_by_query_value(query)
    self.main_window_model.stop_query(id)
    self.main_window_model.delete_from_storage(id)
    self.main_window_view.remove_entry(item)
    self._unmap_id_to_item(id)
    self.main_window_view.set_query_count(self.main_window_view.get_query_count() - 1)

  def setup_entry_signals(self, item, entry):
    entry.pause_clicked.connect(self.pause_clicked)
    entry.resume_clicked.connect(self.resume_clicked)
    entry.stop_clicked.connect(self.stop_clicked)

  def pause_clicked(self, entry, query):
    query.state = TaskState.PAUSED
    self._update_entry(query.id, query)
    self.main_window_model.pause_query(query.id)

  def resume_clicked(self, entry, query):
    query.state = TaskState.RESUMED
    self._update_entry(query.id, query)
    self.main_window_model.resume_query(query.id)

  def stop_clicked(self, entry, query):
    self._remove_entry(query.id, query)

class MainWindowModel:

  def __init__(self, scheduler, user_storage, query_storage, emailer, reddit):
    self.scheduler = scheduler
    self.user_storage = user_storage
    self.query_storage = query_storage
    self.emailer = emailer
    self.reddit = reddit

  def user_exist(self):
    return self.user_storage.read_all(default=None) is not None

  def get_querylisting(self):
    self.scheduler.schedule_task(Task(lambda: self.query_storage.read_all(default=RedditQueryListing()),
                                      trigger=TaskTrigger.ONE_OFF, name=TaskName.READ_QUERYLISTING))

  def get_query_by_id(self, id):
    self.scheduler.schedule_task(Task(lambda: self.query_storage.read_by_key(id), trigger=TaskTrigger.ONE_OFF,
                                      name=TaskName.READ_QUERY))

  def get_query_by_id_immediate(self, id):
    return self.query_storage.read_by_key(id)

  def search_reddit(self, querylisting):
    for id, query in querylisting.listing.items():
      self.scheduler.schedule_task(Task(lambda: self.reddit.query(query), trigger=TaskTrigger.INTERVAL,
                                        name=TaskName.QUERY_REDDIT, id=query.id, trigger_args={Time.MIN: 1}))

  def update_storage(self, id, query):
    self.scheduler.schedule_task(Task(lambda: self.query_storage.update(id, query, RedditQueryListing()),
                                 trigger=TaskTrigger.ONE_OFF, name=TaskName.UPDATE_QUERY))

  def delete_from_storage(self, id):
    self.scheduler.schedule_task(Task(lambda: self.query_storage.delete(id, RedditQueryListing()), trigger=TaskTrigger.ONE_OFF,
                                 name=TaskName.DELETE_QUERY))

  def update_query_task(self, id, query):
    self.scheduler.update_task_by_id(id, lambda: self.reddit.query(query))

  def has_existing_queries(self):
    return self.scheduler.task_count() != 0

  def pause_query(self, id):
    self.scheduler.pause_task_by_id(id)

  def resume_query(self, id):
    self.scheduler.resume_task_by_id(id)

  def stop_query(self, id):
    self.scheduler.stop_task_by_id(id)

  def send_email_notification(self, query, posts):
    user = self.user_storage.read_all(User())
    email = RedditEmail(self.emailer.client.email, user.email)
    email.create_message(query, posts)
    self.scheduler.schedule_task(Task(lambda: self.emailer.send(email), trigger=TaskTrigger.ONE_OFF,
                                      name=TaskName.EMAIL_QUERY_RESULT))
