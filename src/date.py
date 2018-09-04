import time
from datetime import datetime
from dateutil import relativedelta as rdelta

class DateTime:

  YEAR = 'year'
  MONTH = 'month'
  DAY = 'day'
  HOUR = 'hour'
  MINUTE = 'minute'
  SECOND = 'second'
  PLURAL = 's'

  @staticmethod
  def now():
    return time.time()

  @staticmethod
  def elapsed(start, end):
    date_time_start = datetime.fromtimestamp(start)
    date_time_end = datetime.fromtimestamp(end)
    relative_date = rdelta.relativedelta(date_time_end, date_time_start)
    return DateTime.largest_time_period(relative_date)

  @staticmethod
  def largest_time_period(date):
    period_format = "{} {}"
    if date.years:
      year = DateTime.YEAR if date.years is 1 else DateTime.YEAR + DateTime.PLURAL
      return period_format.format(date.years, year)
    if date.months:
      month = DateTime.MONTH if date.months is 1 else DateTime.MONTH + DateTime.PLURAL
      return period_format.format(date.months, month)
    if date.days:
      day = DateTime.DAY if date.days is 1 else DateTime.DAY + DateTime.PLURAL
      return period_format.format(date.days, day)
    if date.hours:
      hour = DateTime.HOUR if date.hours is 1 else DateTime.HOUR + DateTime.PLURAL
      return period_format.format(date.hours, hour)
    if date.minutes:
      minute = DateTime.MINUTE if date.minutes is 1 else DateTime.MINUTE + DateTime.PLURAL
      return period_format.format(date.minutes, minute)
    second = DateTime.SECOND if date.seconds is 1 else DateTime.SECOND + DateTime.PLURAL
    return period_format.format(date.seconds, second)
