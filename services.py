"""Defines the restful services available to the application."""

__author__ = 'jason'


import endpoints

#from protorpc.wsgi import service

from happy_meter.services import group_service
from happy_meter.services import user_service
import tictactoe_api

# import postservice


# Map the RPC service and path (/PostService)
#application = service.service_mappings([('/services/user.*', services.user_service.UserService)], debug=True)

application = endpoints.api_server([tictactoe_api.TicTacToeApi, group_service.GroupService, user_service.UserService],
                                   restricted=False)
#application = endpoints.api_server([UserService], restricted=False)
