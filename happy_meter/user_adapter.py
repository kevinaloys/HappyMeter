"""API implemented to adapt user messages to models and back again."""


from datetime import date as dt
from datetime import timedelta
import logging as logger
import endpoints
import random

from protorpc import messages
#from protorpc import message_types
from protorpc import remote
from google.appengine.api import users

import happy_meter.model.group as group_model
import happy_meter.model.happiness as happiness_model
import happy_meter.messages.user_messages
import happy_meter.model.user as user_model



__author__ = 'jasonchilders'

# TODO: adapt from UserModel back to UserResponse
class UserAdapter():

  @staticmethod
  def AdaptFromUserResponse(user):
    """Adapts from a UserResponse to a user_model.User model object."""
    logger.info('user.user_name: %s' % user.user_name)
    logger.info('user.happiness: %s' % user.happiness)
    daily_happiness_dataobject = UserAdapter.AdaptFromHappinessResponse(user.daily_happiness)
    logger.info('user.groups: %s' % user.groups)
    groups_dataobject = UserAdapter.AdaptFromGroupResponse(user.groups)
    logger.info('groups_dataobject: %s' % groups_dataobject)
    user_dataobject = user_model.User(name=user.user_name, happiness=user.happiness,
                                      daily_happiness=daily_happiness_dataobject, groups=groups_dataobject)
    #logger.info('user_dataobject: %s' % user_dataobject)
    return user_dataobject

  @staticmethod
  def AdaptFromHappinessResponse(daily_happiness):
    daily_happiness_dataobjects = []

    for days_happiness in daily_happiness:
      days_happiness_dataobject = happiness_model.DailyHappiness(date=UserAdapter._ToDate(days_happiness.date),
                                                                 happiness=days_happiness.mood)
      daily_happiness_dataobjects.append(days_happiness_dataobject)

    #logger.info('daily_happiness_dataobject: %s' % daily_happiness_dataobjects)
    return daily_happiness_dataobjects

  @staticmethod
  def AdaptFromGroupResponse(groups):
    """Adapts from a GroupResponse to a group_model.Group model object."""
    groups_dataobject = []

    #logger.info('groups.size: %d' % len(groups))
    #logger.info('groups: %s' % groups)
    for group in groups:
      #logger.info('group: %s' % group)
      happiness_users_dataobject = UserAdapter.AdaptFromGroupMemberResponse(group)
      group_dataobject = group_model.Group(name=group.group_name, happiness=group.happiness,
                                            users=happiness_users_dataobject)
      groups_dataobject.append(group_dataobject)

    #logger.info('groups_dataobject: %s' % groups_dataobject)
    #logger.info('groups: %s' % groups)
    return groups_dataobject


  @staticmethod
  def AdaptFromGroupMemberResponse(group):
    """Adapts from a GroupMemberResponse to a HappinessUser model object."""
    #logger.info('group.group_name: %s' % group.group_name)
    #logger.info('group.happiness: %s' % group.happiness)
    happiness_users_dataobject = []
    for happiness_user in group.group_members:
      happiness_user_dataobject = happiness_model.HappinessUser(name=happiness_user.user_name,
                                                                happiness=happiness_user.happiness)
      happiness_users_dataobject.append(happiness_user_dataobject)

    return happiness_users_dataobject

  @staticmethod
  def _ToDate(date_str):
    """Returns a date when parsing the date_str of the format YYYY-MM-DD"""
    date_list = date_str.split('-')
    return dt(int(date_list[0]), int(date_list[1]), int(date_list[2]))
