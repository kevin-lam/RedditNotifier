import logging
import pickle

from pickle import PickleError

MODE_READ = 'rb'
MODE_WRITE = 'wb'

class FileStorage:

  def __init__(self, retriever, saver):
    self.retriever = retriever
    self.saver = saver
    self.log = logging.getLogger('storage')

  def read_all(self, default):
    try:
      return self.retriever.get()
    except:
      return default

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
    listing = self.read_all(default)
    listing.add(data)
    self.overwrite(listing)

  def delete(self, key, default):
    listing = self.read_all(default)
    if key in listing.list:
      del listing.list[key]
      self.overwrite(listing)

  def update(self, key, data, default):
    listing = self.read_all(default)
    if key in listing.list:
      listing.list[key] = data
      self.overwrite(listing)


class PickleStorageRetriever:

  def __init__(self, file):
    self.file = file

  def get(self):
    return self._load()

  def _load(self):
    with open(self.file, MODE_READ) as open_file:
      return pickle.load(open_file)


class PickleStorageSaver:

  def __init__(self, file):
    self.file = file

  def put(self, data):
    self._save(data)

  def _save(self, data):
    with open(self.file, MODE_WRITE) as open_file:
      pickle.dump(data, open_file, pickle.HIGHEST_PROTOCOL)
