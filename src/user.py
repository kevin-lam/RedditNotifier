import re

class User:

  def __init__(self, email=''):
    self.email = email

class UserValidator:

  def __init__(self):
    pass

  def user_info_valid(self, user):
    email_valid = self._validate_email(user.email)
    return email_valid

  def _validate_email(self, email):
    return re.match('[^@]+@[^@]+\.[^@]+', email) is not None
