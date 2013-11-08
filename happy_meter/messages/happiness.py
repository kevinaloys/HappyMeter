from protorpc import messages


__author__ = 'jason'


class Happiness(messages.Message):
  username = messages.StringField(1, required=True)
  score = messages.IntegerField(1)



