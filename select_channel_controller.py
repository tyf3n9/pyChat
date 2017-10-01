from http_controller import *
from storage import *


class SelectChannelController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        channel_name = req.params['channel'][0]
        user = req.mw_data['token']['user_obj']

        channel = Storage.get_channel_by_name(channel_name)

        if channel is None:
            res.send_status(404)
            res.send_response('Channel not found')
        else:
            user.set_channel(channel)
            res.send_status(200)
            res.send_response(channel_name)
