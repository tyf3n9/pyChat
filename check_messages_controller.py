import json
from http_controller import *
from storage import *
from api_token import *


class CheckMessagesController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        user_token = req.params['token'][0]
        username = Token.extract_user_name(user_token)
        if username is None:
            res.send_status(403)
            res.send_response('Access forbidden')
        else:
            user = Storage.get_user_by_name(username)

            if user is None:
                res.send_status(403)
                res.send_response('Access forbidden')
            else:
                channel = user.get_channel()

                if channel is None:
                    res.send_status(404)
                    res.send_response('Channel not found')
                else:
                    res.send_status(200)
                    res.send_response(json.dumps(channel.get_messages()))
