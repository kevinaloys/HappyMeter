"""ndb.model class definitions for Users."""

from google.appengine.ext import ndb
from happy_meter.model import group as group_model
from happy_meter.model import happiness as happiness_model

__author__ = 'jason'


BASE_HAPPINESS = 100


class User(ndb.Model):

  name = ndb.StringProperty()
  # a user's happiness is initially set to 100, and then computed based on each daily addition
  happiness = ndb.IntegerProperty()
  daily_happiness = ndb.StructuredProperty(happiness_model.DailyHappiness, repeated=True)
  groups = ndb.LocalStructuredProperty(group_model.Group, repeated=True)
  created_dt = ndb.DateTimeProperty(auto_now_add=True)
  last_updated_dt = ndb.DateTimeProperty(auto_now=True)

  @staticmethod
  def Create(name, groups=None):
    user = User(name=name, happiness=BASE_HAPPINESS, groups=groups)
    return user.put()

  @staticmethod
  def CalculateHappiness(current_happiness, daily_happiness):
    calculated_happiness = current_happiness
    if daily_happiness is not None:
      calculated_happiness = BASE_HAPPINESS
      for days_happiness in daily_happiness:
        calculated_happiness = calculated_happiness + days_happiness.happiness

    return calculated_happiness