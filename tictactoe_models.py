"""Helper model class for TicTacToe API.

Defines models for persisting and querying score data on a per user basis and
provides a method for returning a 401 Unauthorized when no current user can be
determined.
"""


__author__ = 'jason'


import endpoints
import logging as logger

from google.appengine.ext import ndb

from tictactoe_api_messages import ScoreResponseMessage


TIME_FORMAT_STRING = '%b %d, %Y %I:%M:%S %p'


def get_endpoints_current_user(raise_unauthorized=False):
    """Returns a current user and (optionally) causes an HTTP 401 if no user.

    Args:
        raise_unauthorized: Boolean; defaults to True. If True, this method
            raises an exception which causes an HTTP 401 Unauthorized to be
            returned with the request.

    Returns:
        The signed in user if there is one, else None if there is no signed in
        user and raise_unauthorized is False.
    """
    current_user = endpoints.get_current_user()
    logger.info('current_user: %s' % current_user)
    #if current_user is None:
    #  current_user = 'jason'
    if raise_unauthorized and current_user is None:
        raise endpoints.UnauthorizedException('Invalid token.')
    return current_user


class Score(ndb.Model):
    """Model to store scores that have been inserted by users.

    Since the played property is auto_now_add=True, Scores will document when
    they were inserted immediately after being stored.
    """
    outcome = ndb.StringProperty(required=True)
    played = ndb.DateTimeProperty(auto_now_add=True)
    #player = ndb.UserProperty(required=True)
    player = ndb.StringProperty(required=True)

    @property
    def timestamp(self):
        """Property to format a datetime object to string."""
        return self.played.strftime(TIME_FORMAT_STRING)

    def to_message(self):
        """Turns the Score entity into a ProtoRPC object.

        This is necessary so the entity can be returned in an API request.

        Returns:
            An instance of ScoreResponseMessage with the ID set to the datastore
            ID of the current entity, the outcome simply the entity's outcome
            value and the played value equal to the string version of played
            from the property 'timestamp'.
        """
        return ScoreResponseMessage(id=self.key.id(),
                                    outcome=self.outcome,
                                    played=self.timestamp)

    @classmethod
    def put_from_message(cls, message):
        """Gets the current user and inserts a score.

        Args:
            message: A ScoreRequestMessage instance to be inserted.

        Returns:
            The Score entity that was inserted.
        """
        current_user = get_endpoints_current_user()
        if current_user is None:
          current_user = 'jason'
        logger.info('current_user: %s' % current_user)
        entity = cls(outcome=message.outcome, player=current_user)
        entity.put()
        return entity

    @classmethod
    def query_current_user(cls):
        """Creates a query for the scores of the current user.

        Returns:
            An ndb.Query object bound to the current user. This can be used
            to filter for other properties or order by them.
        """
        current_user = get_endpoints_current_user()
        return cls.query(cls.player == current_user)
