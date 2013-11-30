"""ProtoRPC message class definitions for GroupService API."""


__author__ = 'jason'


from protorpc import messages


# Create the request string containing the group's name
class GroupRequest(messages.Message):
    group_name = messages.StringField(1, required=True)


class GroupMemberResponse(messages.Message):
    user_name = messages.StringField(1, required=True)
    happiness = messages.IntegerField(2, required=True)


# Create the response string
class GroupResponse(messages.Message):
    group_name = messages.StringField(1, required=True)
    happiness = messages.IntegerField(2, required=True)
    group_members = messages.MessageField(GroupMemberResponse, 3, required=False, repeated=True)