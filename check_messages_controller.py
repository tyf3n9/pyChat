import json
from http_controller import *


class CheckMessagesController(HTTPController):
    def handle_route(self, req: HTTPRequest, res: HTTPResponse):
        user = req.mw_data['token']['user_obj']

        channel = user.get_channel()

        if channel is None:
            res.send_status(404)
            res.send_response('Channel not found')
        else:
            res.send_status(200)
            res.send_response(json.dumps(channel.get_messages()))
