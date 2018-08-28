import pytest
import sys
import mock

sys.path.append('..')

from pickle import PickleError
from storage import PickleStorageRetriever, PickleStorageSaver, FileStorage
class Listing:
  list = []
  def add(self, data):
    self.list.append(data)


class TestFileStorage:

  @pytest.fixture(scope="function")
  def mock_storage(self):
    retriever = mock.create_autospec(PickleStorageRetriever)
    saver = mock.create_autospec(PickleStorageSaver)
    return FileStorage(retriever, saver)

  def test_read_all_success(self, mock_storage):
    mock_storage.retriever.get.return_value = 'success'
    assert mock_storage.read_all(None) is 'success'

  def test_read_all_could_not_read(self, mock_storage):
    mock_storage.retriever.get.side_effect = PickleError()
    assert mock_storage.read_all(None) is None

  def test_read_by_key(self, mock_storage):
    mock_listing = mock.Mock()
    mock_listing.get.return_value = 'success'
    mock_storage.retriever.get.return_value = mock_listing
    assert mock_storage.read_by_key('test') is 'success'

  def test_read_by_key_key_doesnt_exist(self, mock_storage):
    mock_storage.retriever.get.side_effect = PickleError()
    assert mock_storage.read_by_key('test') is None

  def test_overwrite_sucess(self, mock_storage):
    mock_storage.overwrite('test')
    mock_storage.saver.put.assert_called_once()

  def test_overwrite_pickle_error(self, mock_storage):
    mock_storage.saver.put.side_effect = PickleError()
    mock_logger = mock.Mock()
    mock_storage.log = mock_logger
    mock_storage.overwrite('test')
    mock_logger.exception.assert_called_once()

  def test_append(self, mock_storage):
    mock_storage.retriever.get.return_value = Listing()
    mock_storage.append('test', None)

  def test_delete(self, mock_storage):
    mock_storage.delete('key', Listing())

  def test_update(self, mock_storage):
    mock_storage.update('key', 'one', Listing())
