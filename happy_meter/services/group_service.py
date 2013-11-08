"""GroupService API implemented using Google Cloud Endpoints."""


import logging as logger
import endpoints

from protorpc import messages
from protorpc import message_types
from protorpc import remote

import happy_meter.messages.group_messages as group_messages


__author__ = 'jasonchilders'


CLIENT_ID = 'happiemeter'


# Replace GroupRequest with message_types.VoidMessage if no arguments will appear in the request body
GROUP_HAPPINESS_RESOURCE_CONTAINER = endpoints.ResourceContainer(
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
    group_name = request.group_name
    logger.info('group_name: %s' % group_name)
    group_message = group_messages.GroupResponse(group_name=group_name, happiness=100)
    return group_message
