class SendMailFailureException(Exception):
  RECEIVER_DENIED_EMAIL = 'Nobody received the email'
  SERVER_NO_REPLY = 'Server did not reply'
  YOUR_ADDR_DENIED = 'Your email address was not accepted'
  SERVER_UNEXPECTED_ERROR = 'Server experienced an error outside of refusing sender'

  def __init__(self, message):
    self.message = message


class RedditAccessException(Exception):
  GENERAL_CLIENT = 'General error client side.'
  GENERAL_SERVER = 'General error server side.'
  CODE_FAILURE = 'Code to exexcute cannot be completed.'
  OAUTH_ERROR = 'OAuthentication2 error.'
  INVALID_JSON = 'Response did not contain valid JSON.'
  INVALID_PARAM = 'Request did not contain valid parameters.'
  CONFLICT_OF_RESOURCES = 'Conflicting change in target resource.'
  AUTHENTICATION_FAILURE = 'Authentication is not permitted for request.'
  SCOPE_FAILURE = 'Request requires different scope.'
  INVALID_TOKEN = 'Request used invalid token.'
  INVALID_URL = 'Requested url not found.'
  REDIRECT = 'Request resulted in a redirect.'
  SERVER_ERROR = 'Error on server end.'
  SPAM_PREVENTION = 'Spam-prevention prevented request.'
  INCOMING_DATA_TOO_LARGE = 'Request data exceeded limit.'
  URL_ILLEGAL = 'Requested url unavailable due to legal reasons.'

  def __init__(self, message):
    self.message = message
