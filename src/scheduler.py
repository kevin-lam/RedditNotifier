from enum import Enum

class TaskScheduler:
  def __init__(self, scheduler):
    self.scheduler = scheduler

  def schedule_task_in_interval(self, task, amount, unit):
    job = self.scheduler.add_job(task.to_run(), 'interval', **{unit: amount})
    task.store_scheduled_job(job)
    return task

  def cancel_scheduled_task(self, task):
    task.cancel()


class Task:
  def __init__(self, func):
    self.scheduled_job = None
    self.function_to_run = func
    self.running_state = TaskState.STOPPED

  def store_scheduled_job(self, job):
    self.scheduled_job = job
    self.running_state = TaskState.RUNNING

  def to_run(self):
    return self.function_to_run

  def cancel(self):
    if self.is_active():
      self.scheduled_job.remove()
      self.running_state = TaskState.STOPPED

  def is_active(self):
    return self.running_state == TaskState.RUNNING


class TaskState(Enum):
  STOPPED = 1
  PAUSED = 2
  RUNNING = 3

class Time:
  MIN = 'minutes'
  HR = 'hours'
  SEC = 'seconds'
  DAY = 'days'
