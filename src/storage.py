import logging
import pickle
import os

from pickle import PickleError
from lock import ReadWriteLock

MODE_READ = 'rb'
MODE_WRITE = 'wb'
lock = ReadWriteLock()

class FileStorage:

  def __init__(self, retriever, saver):
    self.retriever = retriever
    self.saver = saver
    self.log = logging.getLogger('storage')

  def read_all(self, default):
    return self.retriever.get(default)

  def read_by_key(self, key):
    listing = self.read_all(None)
    if listing is None:
      return None
    return listing.get(key)

  def overwrite(self, data):
    try:
      self.saver.put(data)
    except PickleError as pe:
      self.log.exception(str(pe))

  def append(self, data, default):
    queries = self.read_all(default)
    queries.add(data)
    self.overwrite(queries)

  def delete(self, key, default):
    queries = self.read_all(default)
    if queries.contains(key):
      queries.remove(key)
      self.overwrite(queries)

  def update(self, key, data, default):
    queries = self.read_all(default)
    if queries.contains(key):
      queries.set(key, data)
      self.overwrite(queries)


class PickleStorageRetriever:

  def __init__(self, file):
    self.file = file

  def get(self, default):
    lock.r_lock()
    load_result = self._load(default)
    lock.r_unlock()
    return load_result

  def _load(self, default):
    if os.path.isfile(self.file):
      with open(self.file, MODE_READ) as open_file:
        try:
          return pickle.load(open_file)
        except Exception:
          pass
    with open(self.file, MODE_WRITE) as open_file:
      pickle.dump(default, open_file)
    return default

class PickleStorageSaver:

  def __init__(self, file):
    self.file = file

  def put(self, data):
    lock.w_lock()
    self._save(data)
    lock.w_unlock()

  def _save(self, data):
    with open(self.file, MODE_WRITE) as open_file:
      pickle.dump(data, open_file, pickle.HIGHEST_PROTOCOL)
