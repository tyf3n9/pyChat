import json
from http_controller import *
from storage import *


class ChannelListController(HTTPController):
    def handle_route(self, req: HTTPRequest, res: HTTPResponse) -> None:
        res.send_status(200)
        res.end_headers()
        res.send_response(json.dumps(Storage.get_channel_list()))
