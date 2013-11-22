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

from happy_meter.messages import group_messages
from happy_meter.messages import user_messages
import happy_meter.model.group as group_model
import happy_meter.model.happiness as happiness_model
import happy_meter.model.user as user_model



__author__ = 'jasonchilders'

# TODO: adapt from UserModel back to UserResponse
class UserAdapter():

  #class UserResponse(messages.Message):
  #  user_name = messages.StringField(1, required=True)
  #  happiness = messages.IntegerField(2, required=True)
  #  daily_happiness = messages.MessageField(HappinessResponse, 3, required=False, repeated=True)
  #  groups = messages.MessageField(group_messages.GroupResponse, 4, required=False, repeated=True)

  #class User(ndb.Model):
  #  name = ndb.StringProperty()
  #  # a user's happiness is initially set to 100, and then computed based on each daily addition
  #  happiness = ndb.IntegerProperty()
  #  daily_happiness = ndb.StructuredProperty(happiness_model.DailyHappiness, repeated=True)
  #  groups = ndb.LocalStructuredProperty(group_model.Group, repeated=True)
  #  created_dt = ndb.DateTimeProperty(auto_now_add=True)
  #  last_updated_dt = ndb.DateTimeProperty(auto_now=True)

  #class DailyHappiness(ndb.Model):
  #  date = ndb.DateProperty()
  #  # happiness can be "unhappy", "meh", or "happy" on any given day for a value of -1, 0, and 1 respectively
  #  happiness = ndb.IntegerProperty()
  #  created_dt = ndb.DateTimeProperty(auto_now_add=True)
  #  last_updated_dt = ndb.DateTimeProperty(auto_now=True)

  #class HappinessResponse(messages.Message):
  #  date = messages.StringField(1, required=True)
  #  mood = messages.IntegerField(2, required=True)

  #class Group(ndb.Model):
  #  name = ndb.StringProperty()   # ie. friends
  #  happiness = ndb.IntegerProperty()
  #  users = ndb.LocalStructuredProperty(happiness_model.HappinessUser, repeated=True)
  #  created_dt = ndb.DateTimeProperty(auto_now_add=True)
  #  last_updated_dt = ndb.DateTimeProperty(auto_now=True)

  #class GroupResponse(messages.Message):
  #  group_name = messages.StringField(1, required=True)
  #  happiness = messages.IntegerField(2, required=True)
  #  group_members = messages.MessageField(GroupMemberResponse, 3, required=False, repeated=True)

  #class HappinessUser(ndb.Model):
  #  name = ndb.StringProperty()
  #  happiness = ndb.IntegerProperty()
  #  created_dt = ndb.DateTimeProperty(auto_now_add=True)
  #  last_updated_dt = ndb.DateTimeProperty(auto_now=True)

  #class GroupMemberResponse(messages.Message):
  #  user_name = messages.StringField(1, required=True)
  #  happiness = messages.IntegerField(2, required=True)

  @staticmethod
  def AdaptUserHappinessFromUserModel(user):
    """Adapts from a UserModel to a user_messages.UserResponse messages for user and happiness properties object."""
    logger.info('user.name: %s' % user.name)
    logger.info('user.happiness: %s' % user.happiness)
    user_msg = user_messages.UserResponse(user_name=user.name, happiness=user.happiness)
    return user_msg


  @staticmethod
  def AdaptFromUserModel(user):
    """Adapts from a UserModel to a user_messages.UserResponse messages object."""
    #logger.info('user: %s' % user)
    logger.info('user.name: %s' % user.name)
    logger.info('user.happiness: %s' % user.happiness)

    logger.info('user.daily_happiness: %s' % user.daily_happiness)
    daily_happiness_msg = UserAdapter.AdaptFromDailyHappinessModel(user.daily_happiness)

    logger.info('user.groups: %s' % user.groups)
    groups_msg = UserAdapter.AdaptFromGroupsModel(user.groups)

    user_msg = user_messages.UserResponse(user_name=user.name, happiness=user.happiness,
                                          daily_happiness=daily_happiness_msg, groups=groups_msg)
    return user_msg

  @staticmethod
  def AdaptFromGroupsModel(groups):
    groups_msg = []
    for group_dataobject in groups:
      # get group_members
      group_members_msg = UserAdapter.AdaptFromHappinessUserModel(group_dataobject.users)
      group_msg = group_messages.GroupResponse(group_name=group_dataobject.name, happiness=group_dataobject.happiness,
                                               group_members=group_members_msg)
      groups_msg.append(group_msg)

    return groups_msg

  @staticmethod
  def AdaptFromHappinessUserModel(users):
    group_members_msg = []
    for user in users:
      group_member_msg = group_messages.GroupMemberResponse(user_name=user.name, happiness=user.happiness)
      group_members_msg.append(group_member_msg)

    return group_members_msg

  @staticmethod
  def AdaptFromDailyHappinessModel(daily_happiness):
    daily_happiness_msgs = []
    for dh in daily_happiness:
      happiness_msg = user_messages.HappinessResponse(date=str(dh.date), mood=dh.happiness)
      daily_happiness_msgs.append(happiness_msg)

    return daily_happiness_msgs


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
