import pytest
import sys
import random
import string

sys.path.append('..')

from storage import QueryStorageRetriever, QueryStorageSaver
from reddit import RedditQuery, RedditQueryGroup

TEST_FILE = 'storage_test_file.pckl'

@pytest.fixture(scope='module')
def retriever():
  return QueryStorageRetriever(TEST_FILE)

@pytest.fixture(autouse=True)
def create_query_group_with_five_queries():
  query_group = RedditQueryGroup()

  for i in range(5):
    keyword = random_string_len(5)
    subreddit = random_string_len(8)
    key = keyword + subreddit
    query_group.put(key, create_query(keyword, subreddit))

  saver = QueryStorageSaver(TEST_FILE)
  saver.save(query_group)

def random_string_len(n):
  return ''.join(random.choice(string.lowercase) for x in range(n))

def create_query(keyword, subreddit):
  return RedditQuery(keyword, subreddit)


class TestQueryStorageRetriever:
  def test_get_all(self, retriever):
    queries = retriever.get_all()
    assert queries != None


class TestQueryStorageSaver:
  @pytest.fixture(autouse=True)
  def create_saver(self):
    self.saver = QueryStorageSaver(TEST_FILE)

  def test_save(self, retriever):
    original_size = 5

    query_group = RedditQueryGroup()
    keyword = random_string_len(5)
    subreddit = random_string_len(8)
    key = keyword + subreddit
    query_group.put(key, create_query(keyword, subreddit))

    self.saver.save(query_group)
    query_group = retriever.get_all()
    assert query_group.size() != original_size
