"""ndb.model class definitions for Groups."""

from google.appengine.ext import ndb
#from happy_meter.model import user
from happy_meter.model import happiness as happiness_model

__author__ = 'jason'


class Group(ndb.Model):
  name = ndb.StringProperty()   # ie. friends
  happiness = ndb.IntegerProperty()
  users = ndb.LocalStructuredProperty(happiness_model.HappinessUser, repeated=True)
  created_dt = ndb.DateTimeProperty(auto_now_add=True)
  last_updated_dt = ndb.DateTimeProperty(auto_now=True)

  @staticmethod
  def Create(name, users=None):
    group = Group(name=name, users=users)
    group.happiness = Group.CalculateHappiness(group.users)
    return group.put()

  @staticmethod
  def CalculateHappiness(users):
    total_happiness = 0
    for a_user in users:
      total_happiness = total_happiness + a_user.happiness

    return total_happiness / len(users)