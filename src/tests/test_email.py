import sys

sys.path.append('..')

from mock import Mock
from electronicmail import EmailSender, EmailValidator

class TestEmailSender:
  def test_send(self):
    email_client_mock = Mock()
    email = Mock()

    sender = EmailSender(email_client_mock)
    sender.send(email)

    email_client_mock.sendmail.assert_called()

class TestEmailValidator:
  def test_validate(self):
    validator = EmailValidator()
    assert validator.validate('21test.213_!^%#&^(*blakblak@!#.com') == True
