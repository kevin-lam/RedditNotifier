from exception import SendMailFailureException
from smtplib import SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError

class EmailSender:
  def __init__(self, client):
    self.client = client

  def send(self, email):
    try:
      self.client.sendmail(email.from_email(), email.to_email(), email.body())
    except SMTPRecipientsRefused as rr:
      raise SendFailureException(SendFailureException.RECEIVER_DENIED_EMAIL, rr)
    except SMTPHeloError as he:
      raise SendFailureException(SendFailureException.SERVER_NO_REPLY, he)
    except SMTPSenderRefused as sr:
      raise SendFailureException(SendFailureException.YOUR_ADDR_DENIED, sr)
    except SMTPDataError as de:
      raise SendFailureException(SendFailureException.SERVER_UNEXPECTED_ERROR, de)


class Email:
  def __init__(self, sender, receiver, message):
    self.sender = sender
    self.receiver = receiver
    self.message = message

  def from_email(self):
    return self.sender

  def to_email(self):
    return self.receiver

  def body(self):
    return self.message
