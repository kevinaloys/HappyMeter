from google.appengine.ext import ndb


__author__ = 'jason'


class TestModel(ndb.Model):
  """A model class used for testing."""
  test_id = ndb.IntegerProperty()
  name = ndb.StringProperty()
  unique_name = ndb.StringProperty()


class Person(ndb.Model): # datamodel object
  daily_happiness = ndb.IntegerProperty()
  name = ndb.StringProperty()
  age = ndb.IntegerProperty()
  height = ndb.FloatProperty()

  @staticmethod
  def Create(name, age, daily_happiness):
    #kevin = Person()
    p = Person(name='Sergio', age=12, daily_happiness=1, height=6.1)
    #kevin.name = name
    #kevin.age = age
    #kevin.daily_happiness = daily_happiness
    #return kevin.put()
    return p.put()