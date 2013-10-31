__author__ = 'jason'

from google.appengine.ext import ndb

class TestModel(ndb.Model):
  """A model class used for testing."""
  test_id = ndb.IntegerProperty()
  name = ndb.StringProperty()
  unique_name = ndb.StringProperty()
