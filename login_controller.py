from http_controller import *
from storage import *
from api_token import *


class LoginController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        nickname = req.params['nickname'][0]

        if len(nickname) > 0:
            if not Storage.add_user(nickname):
                res.send_status(409)
                res.send_response('User exists')
            else:
                res.send_status(200)
                token = Token(nickname)
                res.send_response(token.get_token())
