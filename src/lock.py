import threading

class ReadWriteLock:

  def __init__(self):
    self.lock = threading.Condition(threading.Lock())
    self.num_readers = 0

  def r_lock(self):
    self.lock.acquire()
    try:
      self.num_readers +=1
    finally:
      self.lock.release()

  def r_unlock(self):
    self.lock.acquire()
    try:
      self.num_readers -= 1
      if self.num_readers <= 0:
        self.lock.notifyAll()
    finally:
      self.lock.release()

  def w_lock(self):
    self.lock.acquire()
    while self.num_readers > 0:
      self.lock.wait()

  def w_unlock(self):
    self.lock.release()
