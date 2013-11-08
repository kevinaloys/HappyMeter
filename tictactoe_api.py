"""TicTacToe API implemented using Google Cloud Endpoints."""


__author__ = 'jason'


import endpoints
import random
import re

from protorpc import message_types
from protorpc import remote

from tictactoe_models import Score
from tictactoe_api_messages import BoardMessage
from tictactoe_api_messages import ScoresListRequest
from tictactoe_api_messages import ScoresListResponse
from tictactoe_api_messages import ScoreRequestMessage
from tictactoe_api_messages import ScoreResponseMessage
from tictactoe_api_messages import MyResponseMessage


CLIENT_ID = 'happiemeter'


@endpoints.api(name='tictactoe', version='v1',
               description='Tic Tac Toe API',
               allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class TicTacToeApi(remote.Service):
    """Class which defines tictactoe API v1."""

    @staticmethod
    def add_move_to_board(board_state):
        """Adds a random 'O' to a tictactoe board.

        Args:
            board_state: String; contains only '-', 'X', and 'O' characters.

        Returns:
            A new board with one of the '-' characters converted into an 'O';
            this simulates an artificial intelligence making a move.
        """
        result = list(board_state)  # Need a mutable object

        free_indices = [match.start()
                        for match in re.finditer('-', board_state)]
        random_index = random.choice(free_indices)
        result[random_index] = 'O'

        return ''.join(result)

    @endpoints.method(BoardMessage, BoardMessage,
                      path='board', http_method='POST',
                      name='board.getmove')
    def board_get_move(self, request):
        """Exposes an API endpoint to simulate a computer move in tictactoe.

        Args:
            request: An instance of BoardMessage parsed from the API request.

        Returns:
            An instance of BoardMessage with a single 'O' added to the board
            passed in.
        """
        board_state = request.state
        if not (len(board_state) == 9 and set(board_state) <= set('OX-')):
            raise endpoints.BadRequestException('Invalid board.')
        return BoardMessage(state=self.add_move_to_board(board_state))

    @endpoints.method(ScoresListRequest, ScoresListResponse,
                      path='scores', http_method='GET',
                      name='scores.list')
    #@endpoints.method(ScoresListRequest, MyResponseMessage,
    #                  path='scores', http_method='GET',
    #                  name='scores.list')
    def scores_list(self, request):
        """Exposes an API endpoint to query for scores for the current user.

        Args:
            request: An instance of ScoresListRequest parsed from the API
                request.

        Returns:
            An instance of ScoresListResponse containing the scores for the
            current user returned in the query. If the API request specifies an
            order of WHEN (the default), the results are ordered by time from
            most recent to least recent. If the API request specifies an order
            of TEXT, the results are ordered by the string value of the scores.
        """
        query = Score.query_current_user()
        if request.order == ScoresListRequest.Order.TEXT:
            query = query.order(Score.outcome)
        elif request.order == ScoresListRequest.Order.WHEN:
            query = query.order(-Score.played)
        items = [entity.to_message() for entity in query.fetch(request.limit)]
        #my_message = MyResponseMessage(name='jason')
        return ScoresListResponse(items=items)
        #return ScoresListResponse(items=[my_message])
        #return my_message


    @endpoints.method(message_types.VoidMessage, MyResponseMessage,
                      path='name', http_method='GET',
                      name='name.get')
    def GetName(self, request):
        my_message = MyResponseMessage(name='jason')
        return my_message

    @endpoints.method(ScoreRequestMessage, ScoreResponseMessage,
                      path='scores', http_method='POST',
                      name='scores.insert')
    def scores_insert(self, request):
        """Exposes an API endpoint to insert a score for the current user.

        Args:
            request: An instance of ScoreRequestMessage parsed from the API
                request.

        Returns:
            An instance of ScoreResponseMessage containing the score inserted,
            the time the score was inserted and the ID of the score.
        """
        entity = Score.put_from_message(request)
        return entity.to_message()


#application = endpoints.api_server([TicTacToeApi], restricted=False)
