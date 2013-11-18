"""ndb.model class definitions for DailyHappiness"""

from google.appengine.ext import ndb
from datetime import date as dt

__author__ = 'jason'


BASE_HAPPINESS = 100


class HappinessUser(ndb.Model):
  name = ndb.StringProperty()
  happiness = ndb.IntegerProperty()
  created_dt = ndb.DateTimeProperty(auto_now_add=True)
  last_updated_dt = ndb.DateTimeProperty(auto_now=True)

  @staticmethod
  def Create(name, happiness=BASE_HAPPINESS):
    return HappinessUser(name=name, happiness=happiness).put()


class DailyHappiness(ndb.Model):
  date = ndb.DateProperty()
  # happiness can be "unhappy", "meh", or "happy" on any given day for a value of -1, 0, and 1 respectively
  happiness = ndb.IntegerProperty()
  created_dt = ndb.DateTimeProperty(auto_now_add=True)
  last_updated_dt = ndb.DateTimeProperty(auto_now=True)

  @staticmethod
  def Create(happiness, date=None):
    if date is None:
      date =  dt.today()
    the_days_happiness = DailyHappiness(date=date, happiness=happiness)
    return the_days_happiness.put()