import praw
import logging
from prawcore import NotFound
from scheduler import TaskState
from exception import RedditAccessException
from prawcore.exceptions import (
  InvalidInvocation, OAuthException, BadJSON, BadRequest, Conflict, Forbidden,
  InsufficientScope, InvalidToken, NotFound, Redirect, ServerError, SpecialError,
  TooLarge, UnavailableForLegalReasons
)
from praw.exceptions import ClientException, APIException
from date import DateTime

class Reddit:

  def __init__(self, client):
    self.client = client
    self.log = logging.getLogger('reddit')

  def query(self, query):
    try:
      return self._search_subreddit(query.subreddit, query)
    except RedditAccessException as re:
      self.log.exception(re.message)
      return []

  def _search_subreddit(self, subreddit, query):
    result_generator = self._get_subreddit_generator(subreddit, query)
    search_result = []
    for submission in result_generator:
      post = self._create_post_from_submission(submission)
      search_result.append(post)
    return search_result

  def _create_post_from_submission(self, submission):
    try:
      return RedditPost(
        submission.title,
        submission.created_utc,
        submission.num_comments,
        submission.url,
        submission.name
      )
    except ClientException:
      raise RedditAccessException(RedditAccessException.GENERAL_CLIENT)
    except APIException:
      raise RedditAccessException(RedditAccessException.GENERAL_SERVER)
    except InvalidInvocation:
      raise RedditAccessException(RedditAccessException.CODE_FAILURE)
    except OAuthException:
      raise RedditAccessException(RedditAccessException.OAUTH_ERROR)
    except BadJSON:
      raise RedditAccessException(RedditAccessException.INVALID_JSON)
    except BadRequest:
      raise RedditAccessException(RedditAccessException.INVALID_PARAM)
    except Conflict:
      raise RedditAccessException(RedditAccessException.CONFLICT_OF_RESOURCES)
    except Forbidden:
      raise RedditAccessException(RedditAccessException.AUTHENTICATION_FAILURE)
    except InsufficientScope:
      raise RedditAccessException(RedditAccessException.SCOPE_FAILURE)
    except InvalidToken:
      raise RedditAccessException(RedditAccessException.INVALID_TOKEN)
    except NotFound:
      raise RedditAccessException(RedditAccessException.INVALID_URL)
    except Redirect:
      raise RedditAccessException(RedditAccessException.REDIRECT)
    except ServerError:
      raise RedditAccessException(RedditAccessException.SERVER_ERROR)
    except SpecialError:
      raise RedditAccessException(RedditAccessException.SPAM_PREVENTION)
    except TooLarge:
      raise RedditAccessException(RedditAccessException.INCOMING_DATA_TOO_LARGE)
    except UnavailableForLegalReasons:
      raise RedditAccessException(RedditAccessException.URL_ILLEGAL)

  def _get_subreddit_generator(self, subreddit, query):
    return self.client.subreddit(subreddit) \
      .search(
        query=RedditQuery.search_in_field(query.keyword, RedditQuery.TITLE),
        sort=query.sort,
        syntax=query.syntax,
        time_filter=query.time_filter
      )

  def subreddit_exists(self, subreddit):
    exists = False if self._blank_subreddit(subreddit) else True
    try:
      self.client.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
      exists = False
    return exists

  def _blank_subreddit(self, subreddit):
      return subreddit == ''


class RedditPost:

  def __init__(self, title, date, comment_count, link, post_id):
    self.title = title
    self.date = date
    self.comment_count = comment_count
    self.link = link
    self.post_id = post_id


class RedditQuery(object):

  TITLE = 'title'

  def __init__(self, keyword, subreddit, before=None, sort='new', syntax='lucene', time_filter='day'):

    # Fixed reddit search params
    self.keyword = keyword
    self.subreddit = subreddit
    self.sort = sort
    self.syntax = syntax
    self.time_filter= time_filter
    self.id = str(hash(self.keyword + self.subreddit))
    self.total_post_count = 0
    self.state = TaskState.RESUMED
    self.most_recent_post_date = DateTime.now()

  @staticmethod
  def search_in_field(keyword, field):
    keyword_by_field = ''
    for word in keyword.split():
      keyword_by_field += (field + ':' + word + ' ')
    return keyword_by_field


class RedditQueryListing(object):

  def __init__(self):
    self.listing = {}

  def add(self, query):
    self.listing[query.id] = query

  def get(self, key):
    return self.listing[key] if key in self.listing else None

  def set(self, key, data):
    self.listing[key] = data

  def contains(self, key):
    return key in self.listing

  def remove(self, key):
    del self.listing[key]

  def size(self):
    return len(self.listing)
