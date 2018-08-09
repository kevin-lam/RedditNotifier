import pytest
import sys

sys.path.append('..')

from scheduler import Task, TaskScheduler, Time
from apscheduler.schedulers.qt import QtScheduler

def test_func():
  print 'testing!!!!'

class TestTaskScheduler:
  @pytest.fixture(autouse=True)
  def schedule_single_task(self):
    self.scheduler = TaskScheduler(QtScheduler())
    self.task = Task(test_func)
    self.scheduledTask = self.scheduler.schedule_task_in_interval(self.task, 1, Time.SEC)

  def test_schedule_task_in_interval(self):
    assert self.scheduledTask != None

  def test_cancel_scheduled_task(self):
    self.scheduler.cancel_scheduled_task(self.scheduledTask)
    assert self.scheduledTask.is_active() == False
