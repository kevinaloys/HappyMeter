"""UserService API implemented using Google Cloud Endpoints."""


from datetime import date as dt
from datetime import timedelta
import logging as logger
import endpoints
import random

from protorpc import messages
#from protorpc import message_types
from protorpc import remote
from google.appengine.api import users

import happy_meter.messages.user_messages as user_messages


__author__ = 'jasonchilders'


CLIENT_ID = 'happiemeter'


# Replace UserRequest with message_types.VoidMessage if no arguments will appear in the request body
USER_HAPPINESS_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    user_messages.UserRequest, user_name=messages.StringField(1, variant=messages.Variant.STRING, required=True))

USER_GROUP_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    user_messages.UserRequest, user_name=messages.StringField(1, variant=messages.Variant.STRING, required=True),
    group_name=messages.StringField(2, variant=messages.Variant.STRING, required=True))

USER_MOOD_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    user_messages.MoodRequest, mood=messages.StringField(1, variant=messages.Variant.STRING, required=True))

USER_MOOD_RESOURCE_CONTAINER = endpoints.ResourceContainer(
    user_messages.MoodRequest, mood=messages.StringField(1, variant=messages.Variant.STRING, required=True))

#USER_HAPPINESS_RESOURCE_CONTAINER = endpoints.ResourceContainer(
#        message_types.VoidMessage,
#        user_name=messages.StringField(2, variant=messages.Variant.STRING,
#                                       required=True))


@endpoints.api(name='userservice', version='v1', description='User Service API',
               allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class UserService(remote.Service):

  HAPPY = 'happy'
  FLAT = 'flat'
  SAD = 'sad'

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

  #@endpoints.method(user_messages.UserRequest, user_messages.UserResponse, path='user', http_method='POST',
  #                  name='user.create')
  # invoke with: POST http://localhost:8080/_ah/api/userservice/v1/user/create
  #
  # Content-Type:  application/json
  # X-JavaScript-User-Agent:  Google APIs Explorer
  #
  # {
  #  "user_name": "jason"
  # }
  @endpoints.method(USER_HAPPINESS_RESOURCE_CONTAINER, user_messages.UserResponse, path='user/create',
                    http_method='POST', name='user.create')
  def CreateUser(self, request):
    # put the user into the database
    user_name = request.user_name
    logger.info('user_name: %s' % user_name)
    user_message = user_messages.UserResponse(user_name=user_name, happiness=100)
    return user_message

  @endpoints.method(USER_GROUP_RESOURCE_CONTAINER, user_messages.UserResponse,
                    path='user/{user_name}/CreateGroup/{group_name}', http_method='POST', name='user.creategroup')
  def CreateGroup(self, request):
    logger.info('user_name: %s' % request.user_name)
    logger.info('group_name: %s' % request.group_name)
    user_message = user_messages.UserResponse(user_name=request.user_name, happiness=100, group_name=request.group_name)
    return user_message

  @endpoints.method(USER_MOOD_RESOURCE_CONTAINER, user_messages.UserResponse,
                    path='user/happiness/generate/{mood}', http_method='POST', name='user.generatehappiness')
  def GenerateHappiness(self, request):
    user_name = 'jasonchilders@example.com'
    if not user_name:
      user_name = users.get_current_user().email()

    #logger.info('user_name: %s' % users.get_current_user().email())
    logger.info('user_name: %s' % user_name)

    logger.info('mood: %s' % request.mood)
    # generate 270 days of user happiness
    daily_happiness_messages, happiness = UserService.GenerateDailyHappiness(request.mood)

    # TODO: comment this back in when done testing
    #user_message = user_messages.UserResponse(user_name=users.get_current_user().email(), happiness=happiness,
    #                                          daily_happiness=daily_happiness_messages)
    user_message = user_messages.UserResponse(user_name=user_name, happiness=happiness,
                                              daily_happiness=daily_happiness_messages)
    return user_message

  @staticmethod
  def GenerateDailyHappiness(mood):
    daily_happiness = UserService.GenerateRandomMoodDays(mood)
    daily_happiness_messages = []
    happiness = 0
    for key, value in daily_happiness.iteritems():
      daily_happiness_message = user_messages.HappinessResponse(date=key, mood=value)
      daily_happiness_messages.append(daily_happiness_message)
      happiness = happiness + value
    logger.info('daily_happiness: %s' % daily_happiness)
    logger.info('daily_happiness size: %d' % len(daily_happiness))
    logger.info('happiness: %d' % happiness)
    return daily_happiness_messages, happiness

  @staticmethod
  def GenerateDailyMood(mood_type):
    mood = random.randint(1, 99)
    logger.info('random mood: %d' % mood)
    mood = UserService._NormalizeMood(mood_type, mood)
    logger.info('normalized mood: %d' % mood)
    return mood

  @staticmethod
  def _NormalizeMood(mood_type, mood):
    """Flat moods are between sad=1-33, flat=34-66, happy=67-99;
        Happy == sad=1-25, flat=26-50, happy=51-99;
        Sad == sad=1-49; flat=50-74; happy=75-99
    """
    normalized_mood = 0
    if mood_type == UserService.HAPPY:
      if mood <= 25:
        normalized_mood = -1
      elif mood > 25 and mood <= 50:
        normalized_mood = 0
      else:
        normalized_mood = 1
    elif mood_type == UserService.SAD:
      if mood <= 49:
        normalized_mood = -1
      elif mood > 49 and mood <= 74:
        normalized_mood = 0
      else:
        normalized_mood = 1
    else:   # mood_type == UserService.FLAT
      if mood <= 33:
        normalized_mood = -1
      elif mood > 33 and mood <= 66:
        normalized_mood = 0
      else:
        normalized_mood = 1


    return normalized_mood

  @staticmethod
  def GenerateRandomMoodDays(mood_type, days=270):
    """Generate a random mood value for a set of days, using today - 270 as the first day"""
    daily_mood = {}
    delta_days = timedelta(days)
    begin_date = dt.today() - delta_days
    logger.info('begin_date: %s' % begin_date)

    first_days_mood = UserService.GenerateDailyMood(mood_type)
    daily_mood[str(begin_date)] = first_days_mood

    tomorrow = timedelta(1)
    mood_date = begin_date

    for i in range(1, days):
      mood_date = mood_date + tomorrow
      mood = UserService.GenerateDailyMood(mood_type)
      daily_mood[str(mood_date)] = mood

    return daily_mood