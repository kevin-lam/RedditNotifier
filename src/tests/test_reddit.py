import pytest
import sys
import mock
from mock import patch
from praw.exceptions import APIException, ClientException
sys.path.append('..')

from reddit import Reddit, RedditQuery, RedditQueryGroup, RedditQueryRunner

@pytest.fixture(scope='module')
def reddit():
  return Reddit('B78uAmxtKLqu2Q', 'RedditNotifier bot')

class TestReddit():
  @pytest.mark.parametrize('keyword, subreddit', [
    ('test', 'Askreddit'),
    ('', 'Askreddit'),
  ])
  def test_query_reddit_should_return_nonempty(self, reddit, keyword, subreddit):
    query = RedditQuery(keyword=keyword, subreddit=subreddit)
    query_result = reddit.query(query)
    assert query_result != {}


class TestRedditQuery():
  def test_to_string_insert_before_post_id(self):
    keyword = 'test'
    before_post = 'testid'
    subreddit= 'Askreddit'
    query_with_before_added = 'test&before=testid'
    query = RedditQuery(keyword=keyword, subreddit=subreddit, before=before_post)
    assert query.to_string() == query_with_before_added


class TestRedditQueryGroup():
  @pytest.fixture(autouse=True)
  def create_query_group(self):
    self.query_group = RedditQueryGroup()
    keyword = 'test'
    subreddit= 'Askreddit'
    query = RedditQuery(keyword, subreddit)
    self.query_group.put(keyword + subreddit, query)

  def test_put(self):
    keyword = 'test2'
    subreddit= 'Askreddit2'
    query = RedditQuery(keyword, subreddit)
    self.query_group.put(keyword + subreddit, query)
    assert self.query_group.size() == 2

  def test_get(self):
    assert self.query_group.get('testAskreddit') != None

  def test_remove(self):
    self.query_group.remove('testAskreddit')
    assert self.query_group.size() == 0


class TestRedditQueryRunner():
  @pytest.mark.parametrize('subreddit, exists', [
    ('tesstqwiejqoid', False),    # Unknown subreddit
    ('', False),                  # Blank subreddit
    ('mfa', True),                # Abbreviated subreddit
    ('malefashionadvice', True)   # Full subreddit
  ])
  def test_subreddit_exists(self, reddit, subreddit, exists):
    assert reddit.subreddit_exists(subreddit) == exists
