
from api_token import Token
from storage import *
from http_controller import *


class LoginController(HTTPController):
    def handle_route(self, req: HTTPRequest, res: HTTPResponse):
        nick_name = req.params['nickname'][0]

        if len(nick_name) > 0:
            if not Storage.add_user(nick_name):
                res.send_status(409)
                res.send_response('User exists')
            else:
                res.send_status(200)

                req.cookies['token'] = Token.generate_token_str(nick_name, Token.SESSION_TIME)
                req.cookies['refresh_token'] = Token.generate_token_str(nick_name, Token.LONG_SESSION_TIME)
                res.send_cookie(req.cookies)
                res.end_headers()

