import pytest
import sys
import mock

sys.path.append('..')

from reddit import Reddit
from prawcore.exceptions import OAuthException
from prawcore import NotFound

class Submission:

  def __init__(self, title, date, source, comment_count, post_id):
    self.title = title
    self.date = date
    self.source = source
    self.comment_count = comment_count
    self.post_id = post_id

submission = [
  Submission('title1', 'date1', 'source1', 1, 'a'),
  Submission('title2', 'date2', 'source2', 2, 'b'),
  Submission('title3', 'date3', 'source3', 3, 'c')
]

class TestReddit:

  @pytest.fixture(scope="function")
  def mock_reddit(self):
    client = mock.Mock()
    return Reddit(client)

  def test_query_when_success(self, mock_reddit):
    mock_query = mock.MagicMock()
    mock_subreddit = mock.Mock()
    mock_reddit.client.subreddit.return_value = mock_subreddit
    mock_subreddit.search.return_value = iter(submission)
    assert len(mock_reddit.query(mock_query)) is 3

  def test_query_when_failure(self, mock_reddit):
    mock_query = mock.MagicMock()
    mock_subreddit = mock.Mock()
    mock_reddit.client.subreddit.return_value = mock_subreddit
    mock_submission = mock.MagicMock()
    mock_title = mock.PropertyMock(side_effect=OAuthException('test', 'test', 'test'))
    type(mock_submission).title = mock_title
    mock_subreddit.search.return_value = iter([mock_submission])
    assert not mock_reddit.query(mock_query)

  def test_subreddit_exists_when_exists(self, mock_reddit):
    mock_subreddits = mock.Mock()
    mock_reddit.client.subreddits.return_value = mock_subreddits
    mock_reddit.subreddit_exists('testsubreddit')
    mock_reddit.client.subreddits.search_by_name.assert_called_once()

  def test_subreddit_exists_when_doesnt_exists(self, mock_reddit):
    mock_subreddits = mock.Mock()
    mock_reddit.client.subreddits.return_value = mock_subreddits
    mock_reddit.client.subreddits.search_by_name.side_effect = NotFound(mock.Mock())
    assert mock_reddit.subreddit_exists('testsubreddit') is False


