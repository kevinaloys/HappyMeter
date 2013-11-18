"""GroupService API implemented using Google Cloud Endpoints."""


import logging as logger
import endpoints
import random

from protorpc import messages
#from protorpc import message_types
from protorpc import remote
from google.appengine.api import users

import happy_meter.messages.group_messages as group_messages
#import happy_meter.messages.user_messages as user_messages
from happy_meter.messages import  user_messages
#from happy_meter.model import user as user_model
import happy_meter.model.user as user_model


__author__ = 'jasonchilders'


CLIENT_ID = 'happiemeter'


# Replace GroupRequest with message_types.VoidMessage if no arguments will appear in the request body
GROUP_HAPPINESS_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    group_messages.GroupRequest, group_name=messages.StringField(1, variant=messages.Variant.STRING, required=True))

GROUP_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    group_messages.GroupRequest, group_name=messages.StringField(1, variant=messages.Variant.STRING, required=True))

#GROUP_HAPPINESS_RESOURCE_CONTAINER = endpoints.ResourceContainer(
#        message_types.VoidMessage,
#        group_name=messages.StringField(2, variant=messages.Variant.STRING,
#                                        required=True))


@endpoints.api(name='groupservice', version='v1', description='Group Service API',
               allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class GroupService(remote.Service):

  #@endpoints.method(YOUR_RESOURCE_CONTAINER, YourResponseMessageClass,
  #                  path='yourApi/{times}', http_method='GET',
  #                  name='greetings.getGreeting')

  #@endpoints.method(group_messages.GroupRequest, group_messages.GroupResponse, path='group', http_method='GET',
  #                  name='group.gethappiness')
  # invoke with: http://localhost:8080/_ah/api/groupservice/v1/group/${group_name}
  @endpoints.method(GROUP_HAPPINESS_RESOURCE_CONTAINER, group_messages.GroupResponse, path='group/{group_name}',
                    http_method='GET', name='group.getgrouphappiness')
  def GetGroupHappiness(self, request):
    # do something with the request (like get the group's happiness
    group_name = request.group_name
    logger.info('getting happiness for group: %s' % group_name)
    group_message = group_messages.GroupResponse(group_name=group_name, happiness=350)
    return group_message

  #@endpoints.method(group_messages.GroupRequest, group_messages.GroupResponse, path='group', http_method='POST',
  #                  name='group.create')
  # invoke with: POST http://localhost:8080/_ah/api/groupservice/v1/group/create
  #
  # Content-Type:  application/json
  # X-JavaScript-User-Agent:  Google APIs Explorer
  #
  # {
  #  "group_name": "my friends"
  # }
  @endpoints.method(GROUP_HAPPINESS_RESOURCE_CONTAINER, group_messages.GroupResponse, path='group/create',
                    http_method='POST', name='group.create')
  def CreateGroup(self, request):
    # put the group into the database
    user = users.get_current_user()
    logger.info('user: %s' % user)
    group_name = request.group_name
    logger.info('group_name: %s' % group_name)
    group_message = group_messages.GroupResponse(group_name=group_name, happiness=100)
    return group_message

  @endpoints.method(GROUP_RESOURCE_CONTAINER, user_messages.UserResponse, path='group/generate/{group_name}',
                    http_method='POST', name='group.generategroup')
  def GenerateGroup(self, request):
    logger.info('user_name: %s' % users.get_current_user().email())
    logger.info('group_name: %s' % request.group_name)
    # generate a random sized group of 10-70 users with a random happiness between 50 and 370 (370=100+270)
    group_size = GroupService.CreateRandomGroupSize()
    logger.info('group_size: %d' % group_size)
    for i in range(group_size):
      # create a user with happiness
      group_user_name = 'user_' + str(i)
      logger.info('group_user_name: %s' % group_user_name)
      group_user_happiness = GroupService.GenerateRandomHappiness()
      logger.info('group_user_happiness: %d' % group_user_happiness)

      # create User model object
      gen_user = user_model.User(name=group_user_name, happiness=group_user_happiness)
      #logger.info('gen_user: %s' % gen_user)

      # add user to logged-in user's group


    user_group_message = user_messages.UserResponse(user_name=users.get_current_user().email(), happiness=100,
                                                    group_name=request.group_name)
    return user_group_message

  @staticmethod
  def CreateRandomGroupSize():
    size = random.randint(10, 70)
    logger.info('random group size: %d' % size)
    return size

  @staticmethod
  def GenerateRandomHappiness():
    happiness = random.randint(50, 370)
    logger.info('random happiness: %d' % happiness)
    return happiness
