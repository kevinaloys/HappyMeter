"""ProtoRPC message class definitions for TicTicToe API."""


__author__ = 'jason'


from protorpc import messages


class BoardMessage(messages.Message):
    """ProtoRPC message definition to represent a board."""
    state = messages.StringField(1, required=True)


class ScoresListRequest(messages.Message):
    """ProtoRPC message definition to represent a scores query."""
    limit = messages.IntegerField(1, default=10)
    class Order(messages.Enum):
        WHEN = 1
        TEXT = 2
    order = messages.EnumField(Order, 2, default=Order.WHEN)


class ScoreRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a score to be inserted."""
    outcome = messages.StringField(1, required=True)


class ScoreResponseMessage(messages.Message):
    """ProtoRPC message definition to represent a score that is stored."""
    id = messages.IntegerField(1)
    outcome = messages.StringField(2)
    played = messages.StringField(3)

class MyResponseMessage(messages.Message):
    name = messages.StringField(1)

class ScoresListResponse(messages.Message):
    """ProtoRPC message definition to represent a list of stored scores."""
    #items = messages.MessageField(ScoreResponseMessage, 1, repeated=True)
    items = messages.MessageField(MyResponseMessage, 1, repeated=True)
