from exception import SendMailFailureException
from smtplib import SMTP, SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError

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


class EmailClient:

  def __init__(self, host, port, email, password):
    self.host = host
    self.port = port
    self.email = email
    self.password = password

  def connect(self):
    self.client = SMTP(self.host, self.port.encode('ascii'))
    #client.connect(self.host, self.port)
    self.client.ehlo()
    self.client.starttls()
    self.client.ehlo()
    self.client.login(self.email, self.password)


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
