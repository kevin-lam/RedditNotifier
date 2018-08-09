import pickle

MODE_READ = 'rb'
MODE_WRITE = 'wb'

class QueryStorageRetriever:
  def __init__(self, file):
    self.file = file

  def get_all(self):
    return self.__load_query_group()

  def __load_query_group(self):
    with open(self.file, MODE_READ) as query_storage:
      return pickle.load(query_storage)


class QueryStorageSaver:
  def __init__(self, file):
    self.file = file

  def save(self, query_group):
    self.__save_query_within_group(query_group)

  def __save_query_within_group(self, query_group):
    with open(self.file, MODE_WRITE) as query_storage:
      pickle.dump(query_group, query_storage, pickle.HIGHEST_PROTOCOL)
