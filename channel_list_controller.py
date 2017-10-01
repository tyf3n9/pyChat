import json
from http_controller import *
from storage import *


class ChannelListController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        res.send_status(200)
        res.send_response(json.dumps(Storage.get_channel_list()))
