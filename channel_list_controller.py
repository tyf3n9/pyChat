import json
from http_controller import *
from storage import *
from api_token import *


class ChannelListController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        user_token = req.params['token'][0]

        if len(user_token) > 0:

            if Token.validate(user_token):
                res.send_status(200)
                res.send_response(json.dumps(Storage.get_channel_list()))

            else:
                res.send_status(403)
                res.send_response('Access forbidden')

