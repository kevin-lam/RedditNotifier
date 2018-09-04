import logging

from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal
from apscheduler.events import EVENT_JOB_EXECUTED

class TaskScheduler(QObject):

  user_ready = pyqtSignal()
  query_ready = pyqtSignal(str)
  query_available = pyqtSignal(object)
  querylisting_available = pyqtSignal(object)
  query_result_available = pyqtSignal(str, object)

  def __init__(self, scheduler):
    super(TaskScheduler, self,).__init__()
    self.scheduler = scheduler
    self.tasks = {}
    self.log = logging.getLogger("scheduler")
    self.setup()

  def setup(self):
    self._add_callback()
    self.scheduler.start()

  def _add_callback(self):
    self.scheduler.add_listener(self._schedule_task_callback, EVENT_JOB_EXECUTED)

  def schedule_task(self, task):
    job = self.scheduler.add_job(task.to_run(), trigger=task.trigger, args=task.args, id=task.id, **task.trigger_args)
    task.store_scheduled_job(job)
    self._add_task_to_tasks(task)
    return task

  def _add_task_to_tasks(self, task):
    self.tasks[task.id] = task

  def _remove_task_from_tasks(self, task):
    del self.tasks[task.id]

  def _schedule_task_callback(self, event):
    id = event.job_id
    task = self.tasks[id]
    if task.name is TaskName.OVERWRITE_USER:
      self._when_user_ready()
    elif task.name is TaskName.APPEND_QUERY:
      self._when_query_ready(id)
    elif task.name is TaskName.READ_QUERY:
      self._with_query(event.retval)
    elif task.name is TaskName.READ_QUERYLISTING:
      self._with_querylisting(event.retval)
    elif task.name is TaskName.QUERY_REDDIT:
      self._with_query_result(id, event.retval)

    if task.is_one_off() and task.id in self.tasks:
      self._remove_task_from_tasks(task)

  def pause_task_by_id(self, id):
    if id in self.tasks:
      task = self.tasks[id]
      task.scheduled_job.pause()
      task.state = TaskState.PAUSED

  def resume_task_by_id(self, id):
    if id in self.tasks:
      task = self.tasks[id]
      task.scheduled_job.resume()
      task.state = TaskState.RESUMED

  def stop_task_by_id(self, id):
    if id in self.tasks:
      task = self.tasks[id]
      task.scheduled_job.remove()
      del self.tasks[id]

  def update_task_by_id(self, id, function):
    if id in self.tasks:
      task = self.tasks[id]
      task.function_to_run = function
      task.scheduled_job = task.scheduled_job.modify(func=function)

  def task_count(self):
    return len(self.tasks)

  def _when_user_ready(self):
    self.user_ready.emit()

  def _when_query_ready(self, id):
    self.query_ready.emit(id)

  def _with_query(self, query):
    self.query_available.emit(query)

  def _with_querylisting(self, querylisting):
    self.querylisting_available.emit(querylisting)

  def _with_query_result(self, id, query_result):
    self.query_result_available.emit(id, query_result)


class Task:

  def __init__(self, func, trigger, name, id=None, trigger_args={}, args=None):
    self.scheduled_job = None
    self.function_to_run = func
    self.trigger = trigger
    self.name = name
    self.trigger_args = trigger_args
    self.args = args
    self.running_state = TaskState.STOPPED
    self.id = str(hash(self)) if id is None else id

  def store_scheduled_job(self, job):
    self.scheduled_job = job
    self.running_state = TaskState.RESUMED

  def to_run(self):
    return self.function_to_run

  def cancel(self):
    if self.is_active():
      self.scheduled_job.remove()
      self.running_state = TaskState.STOPPED

  def is_active(self):
    return self.running_state == TaskState.RESUMED

  def is_one_off(self):
    return self.trigger is TaskTrigger.ONE_OFF

class TaskState(Enum):
  STOPPED = 1
  PAUSED = 2
  RESUMED = 3

class TaskName:
  OVERWRITE_USER = 'Save user task'
  APPEND_QUERY = 'Add query to existing querylisting'
  READ_QUERY = 'Read in query by id'
  READ_QUERYLISTING = 'Ready in all queries'
  UPDATE_QUERY = 'Changes made to query'
  DELETE_QUERY = 'Remove query'
  QUERY_REDDIT = 'Search reddit'
  EMAIL_QUERY_RESULT = 'Sending email of result'

class TaskTrigger:
  INTERVAL = 'interval'
  ONE_OFF = 'date'

class Time:
  MIN = 'minutes'
  HR = 'hours'
  SEC = 'seconds'
  DAY = 'days'
