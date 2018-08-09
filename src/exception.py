class SendMailFailureException(Exception):
  RECEIVER_DENIED_EMAIL = 'Nobody received the email'
  SERVER_NO_REPLY = 'Server did not reply'
  YOUR_ADDR_DENIED = 'Your email address was not accepted'
  SERVER_UNEXPECTED_ERROR = 'Server experienced an error outside of refusing sender'

  def __init__(self, message, error):
    self.message = message
    self.error = error
