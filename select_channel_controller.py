from http_controller import *
from storage import *
from api_token import *


class SelectChannelController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        user_token = req.params['token'][0]
        channel_name = req.params['channel'][0]
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
                channel = Storage.get_channel_by_name(channel_name)

                if channel is None:
                    res.send_status(404)
                    res.send_response('Channel not found')
                else:
                    user.set_channel(channel)
                    res.send_status(200)
                    res.send_response(channel_name)
