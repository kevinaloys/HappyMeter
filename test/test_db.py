__author__ = 'jasonchilders'

import logging as logger
import random
import sys
import unittest
from google.appengine.datastore import datastore_stub_util
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

    def tearDown(self):
      self.testbed.deactivate()

    def testPut(self):
      # persist a test object
      id = random.randint(0, sys.maxint)
      name = 'test' + str(id)
      logger.debug('name: %s' % name)
      test = TestModel(id, name)
      print 'test: %s' % test
      test_key = test.Create()
      self.assertIsNotNone(test_key, ('test_key: %s cannot be None' % test_key))
      return test

    def testGet(self):
      # get a test object
      self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()