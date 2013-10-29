__author__ = 'jason'

from google.appengine.ext import ndb

class TestModel(ndb.Model):
  """A model class used for testing."""
  test_id = ndb.IntegerProperty()
  name = ndb.StringProperty()

  def __init__(self, test_id, name):
    ndb.Model.__init__(self)
    self.test_id = test_id
    self.name = name

  def Get(self):
    key = ndb.Key(self.test_id, self.name)
    return key.get()

  def GetByIdAndName(self, test_id, name):
    key = ndb.Key(test_id, name)
    return key.Get()

  def Create(self):
    return self.put()

  def Replace(self, test_model):
    return self.Update(test_model)

  def Update(self, test_model):
    self.test_id = test_model.test_id
    self.name = test_model.name
    return self.put()

  def Delete(self):
    key = self.Get()
    key.delete()
