"""UserService API implemented using Google Cloud Endpoints."""


import logging as logger
import endpoints

#from google.appengine.ext import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

import happy_meter.messages.user_messages as user_messages


__author__ = 'jasonchilders'


CLIENT_ID = 'happiemeter'


# Replace UserRequest with message_types.VoidMessage if no arguments will appear in the request body
USER_HAPPINESS_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    user_messages.UserRequest, user_name=messages.StringField(1, variant=messages.Variant.STRING, required=True))

#USER_HAPPINESS_RESOURCE_CONTAINER = endpoints.ResourceContainer(
#        message_types.VoidMessage,
#        user_name=messages.StringField(2, variant=messages.Variant.STRING,
#                                       required=True))


@endpoints.api(name='userservice', version='v1', description='User Service API',
               allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class UserService(remote.Service):

  #@endpoints.method(YOUR_RESOURCE_CONTAINER, YourResponseMessageClass,
  #                  path='yourApi/{times}', http_method='GET',
  #                  name='greetings.getGreeting')

  #@endpoints.method(user_messages.UserRequest, user_messages.UserResponse, path='user', http_method='GET',
  #                  name='user.gethappiness')
  # invoke with: http://localhost:8080/_ah/api/userservice/v1/user/${user_name}
  @endpoints.method(USER_HAPPINESS_RESOURCE_CONTAINER, user_messages.UserResponse, path='user/{user_name}',
                    http_method='GET', name='user.gethappiness')
  def GetHappiness(self, request):
    # do something with the request (like get the user's happiness
    user_name = request.user_name
    logger.info('getting happiness for user: %s' % user_name)
    user_message = user_messages.UserResponse(user_name=user_name, happiness=350)
    return user_message

  @endpoints.method(user_messages.UserRequest, user_messages.UserResponse, path='user', http_method='POST',
                    name='user.create')
  def CreateUser(self, request):
    # put the user into the database
    user_name = request.user_name
    logger.info('user_name: %s' % user_name)
    user_message = user_messages.UserResponse(user_name=user_name, happiness=100)
    return user_message
