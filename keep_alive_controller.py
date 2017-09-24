from api_token import *
from web_server import *
from storage import *


class KeepAliveController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        token = req.params['token'][0]
        username = Token.extract_user_name(token)
        user = Storage.get_user_by_name(username)

        if len(token) > 0:
            if Token.validate(token) and user is not None:
                user.set_timestamp()
                print('keep alive from:', user.get_name())
                res.send_status(200)
                res.send_response('User is alive')
            else:
                res.send_status(403)
                res.send_response('Please log in')
