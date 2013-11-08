__author__ = 'jasonchilders'

import logging as logger
import random
import sys
import unittest
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from happy_meter.model.test import TestModel

class TestDB(unittest.TestCase):

    def setUp(self):
      # First, create an instance of the Testbed class.
      self.testbed = testbed.Testbed()
      # Then activate the testbed, which prepares the service stubs for use
      self.testbed.activate()
      # Create a consistency policy that will simulate the High Replication consistency foo
      self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
      # Initialize the datastore stub with this policy
      self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

      # setup local test properties
      logger.info('running setUp')
      id = random.randint(0, sys.maxint)
      entity_name = 'test'
      entity_unique_name = entity_name + str(id)
      logger.info('entity_name: %s' % entity_unique_name)
      self.entity = TestModel(test_id=id, name=entity_name, unique_name=entity_unique_name)
      self.entity_key = self.entity.put()

    def tearDown(self):
      self.testbed.deactivate()

    def testPut(self):
      # persist a test object
      logger.info('running testPut')
      test = self.entity
      logger.info('test: %s' % test)
      test_key = test.put()
      logger.info('test_key: %s' % test_key)
      self.assertIsNotNone(test_key, ('test_key: %s cannot be None' % test_key))

    def testGet(self):
      # get a test object
      logger.info('running testGet')
      logger.info('self.entity: %s' % self.entity)
      logger.info('self.entity_key: %s' % self.entity_key)
      logger.info('self.entity.name: %s' % self.entity.name)
      logger.info('self.entity.test_id: %s' % self.entity.test_id)

      #test_key = ndb.Key('TestModel', self.entity.name)
      # hmmm... for some reason ndb.Key(TestModel, self.entity.name) is not working in dev
      test_key = self.entity_key
      logger.info('test_key: %s' % test_key)
      test = test_key.get()
      logger.info('test: %s' % test)
      self.assertIsNotNone(test, ('test: %s cannot be None' % test))

    def testGetById(self):
      logger.info('running testGetById')
      test_key = self.entity.get_by_id(1)
      logger.info('retrieved test_key by id: %s' % test_key)
      self.assertIsNotNone(test_key, ('test_key: %s cannot be None' % test_key))

    def testGetNamespace(self):
      logger.info('running testGetNamespace')
      namespace = self.entity_key.namespace()
      logger.info('namespace: %s' % namespace)
      self.assertIsNotNone(namespace, ('namespace: %s cannot be None' % namespace))

    def testQuery(self):
      logger.info('running testQuery')
      query = TestModel.query(TestModel.name == 'test').order(TestModel.test_id)
      models = query.fetch()
      for model in models:
        logger.info('model: %s' % model)
      self.assertIsNotNone(models, 'models cannot be None')


if __name__ == '__main__':
    unittest.main()