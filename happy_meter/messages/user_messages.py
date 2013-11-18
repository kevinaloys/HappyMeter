"""ProtoRPC message class definitions for UserService API."""


__author__ = 'jason'


from protorpc import messages


# Create the request string containing the user's name
class UserRequest(messages.Message):
    user_name = messages.StringField(1, required=True)

class MoodRequest(messages.Message):
  mood = messages.StringField(1, required=True)


class HappinessResponse(messages.Message):
  date = messages.StringField(1, required=True)
  mood = messages.IntegerField(2, required=True)


# Create the response string
class UserResponse(messages.Message):
    user_name = messages.StringField(1, required=True)
    happiness = messages.IntegerField(2, required=True)
    daily_happiness = messages.MessageField(HappinessResponse, 3, required=False, repeated=True)
    group_name = messages.StringField(4, required=False)
