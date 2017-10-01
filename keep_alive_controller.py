from web_server import *


class KeepAliveController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        user = req.mw_data['token']['user_obj']

        user.set_timestamp()
        print('keep alive from:', user.get_name())
        res.send_status(200)
        res.send_response('User is alive')
