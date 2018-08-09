import sys

sys.path.append('..')

from mock import Mock
from electronicmail import EmailSender

class TestEmailSender:
  def test_send(self):
    email_client_mock = Mock()
    email = Mock()

    sender = EmailSender(email_client_mock)
    sender.send(email)

    email_client_mock.sendmail.assert_called()

