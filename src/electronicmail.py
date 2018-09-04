import sys
import copy

sys.path.append('..')

from exception import SendMailFailureException
from smtplib import SMTP, SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from date import DateTime
from parser import HtmlParser
from inputfile import HtmlFile

class EmailSender:

  def __init__(self, client):
    self.client = client

  def send(self, email):
    try:
      self.client.connect()
      self.client.sendmail(email.from_email(), email.to_email(), email.body())
      self.client.disconnect()
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
    self.client.ehlo()
    self.client.starttls()
    self.client.ehlo()
    self.client.login(self.email, self.password)

  def disconnect(self):
    self.client.quit()

  def sendmail(self, from_email, to_email, message):
    self.client.sendmail(from_email, to_email, message)

class RedditEmail:

  def __init__(self, sender, receiver):
    self.msg = MIMEMultipart()
    self.msg['Subject'] = 'RedditNotifier notification'
    self.msg['From'] = sender
    self.msg['To'] = receiver
    self.sender = sender
    self.receiver = receiver

  def from_email(self):
    return self.sender

  def to_email(self):
    return self.receiver

  def body(self):
    return self.msg.as_string()

  def create_message(self, query, posts):
    html = self._create_html_message(query, posts)
    plain = self._create_plain_message(query, posts)
    html_mime = self._create_mime_text(html, 'html')
    plain_mime = self._create_mime_text(plain, 'plain')
    self.msg.attach(html_mime)
    self.msg.attach(plain_mime)

  def _create_html_message(self, query, posts):
    document_formatting = self._read_in_format(HtmlFile.EMAIL_DOC_FORMAT)
    post_formatting = self._read_in_format(HtmlFile.REDDIT_POST_FORMAT)
    header_formatting = self._read_in_format(HtmlFile.REDDIT_HEADER_FORMAT)
    document = self._create_html_document(document_formatting) \
      ._add_header(header_formatting, query) \
      ._add_posts(post_formatting, posts) \
      ._get_document()
    return document.text()

  def _create_plain_message(self, query, posts):
    message = '{} {}\n'.format(query.keyword, query.subreddit)
    for post in posts:
      message += (post.link + '\n')
    return message

  def _create_mime_text(self, document, type):
    return MIMEText(document, type, 'utf-8')

  def _contains_non_ascii(self, document):
    return not all(ord(c) < 128 for c in document)

  def _read_in_format(self, file):
    return HtmlParser(file)

  def _create_plain_document(self, query, posts):
    message = ''
    for post in posts:
      message += (post.link + ' ')
    return message

  def _create_html_document(self, doc_format):
    self.document = doc_format
    return self

  def _add_header(self, header_format, query):
    self.document.insert('header', header_format)
    self.document.replace_text('{keyword}', query.keyword)
    self.document.replace_text('{subreddit}', query.subreddit)
    return self

  def _add_posts(self, post_format, posts):
    for post in posts:
      post_format_cpy = copy.deepcopy(post_format)
      post_format_cpy.replace_link('{link}', post.link)
      post_format_cpy.replace_text('{title}', post.title)
      post_format_cpy.replace_text('{comment_count}', str(post.comment_count) + ' comments')
      post_format_cpy.replace_text('{date}', DateTime.elapsed(post.date, DateTime.now()))
      self.document.insert('content', post_format_cpy)
    return self

  def _get_document(self):
    return self.document
