from http_controller import *
from storage import *


class SelectChannelController(HTTPController):
    def handle_route(self, req: HTTPRequest, res: HTTPResponse) -> None:
        try:
            channel_name = req.params['channel'][0]
            user = req.mw_data['token']['user_obj']

            channel = Storage.get_channel_by_name(channel_name)

            if channel is None:
                res.send_status(404)
                res.end_headers()
            else:
                user.set_channel(channel)
                res.send_status(200)
                res.end_headers()
                res.send_response(channel_name)
        except KeyError:
            res.send_status(404)
            res.end_headers()
