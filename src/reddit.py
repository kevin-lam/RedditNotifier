﻿import praw
from prawcore import NotFound

class Reddit:
  def __init__(self, id, agent):
    self.query_runner = RedditQueryRunner(id, agent)
    self.most_recent_post_id = None

  def query(self, query):
    return self.query_runner.search_query(query)

  def subreddit_exists(self, subreddit):
    return self.query_runner.subreddit_exists(subreddit)


class RedditQuery:
  def __init__(self, keyword, subreddit, before=None, sort='new', syntax='lucene', time_filter='hour'):
    self.variable_query_params = {}
    # Variable reddit search params
    self.variable_query_params['before'] = before

    # Fixed reddit search params
    self.keyword = keyword
    self.subreddit = subreddit
    self.sort = sort
    self.syntax = syntax
    self.time_filter= time_filter

  def to_string(self):
    return self.__concat_keyword_with_variable_query_params()

  def __concat_keyword_with_variable_query_params(self):
    variable_params = ''
    for parameter, value in self.variable_query_params.iteritems():
      if self.__variable_param_exists(value):
        variable_params += self.__join_param(parameter, value) # In the form of &parameter=value
    return self.keyword + variable_params

  def __variable_param_exists(self, value):
    return value != None

  def __join_param(self, param, value):
    return '&' + param + '=' + value

  def sort_by(self):
    return self.sort

  def search_with(self):
    return self.syntax

  def time_filter_by(self):
    return self.time_filter

  def get_subreddit(self):
    return self.subreddit


class RedditQueryRunner:
  def __init__(self, id, agent):
    self.id = id
    self.agent = agent
    self.client = praw.Reddit(client_id=id, client_secret=None, user_agent=agent)

  def search_query(self, query):
    query_string = query.to_string()
    subreddit = query.get_subreddit()
    sort = query.sort_by()
    syntax = query.search_with()
    time_filter = query.time_filter_by()

    if self.subreddit_exists(subreddit):
      return self.client.subreddit(subreddit).search(query_string, sort=sort, syntax=syntax, time_filter=time_filter)
    return {}

  def subreddit_exists(self, subreddit):
    exists = False if self.__blank_subreddit(subreddit) else True
    try:
      self.client.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
      exists = False
    return exists

  def __blank_subreddit(self, subreddit):
      return subreddit == ''
