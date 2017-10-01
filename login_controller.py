from http_controller import *
from storage import *
from api_token import Token


class LoginController(HTTPController):
    @staticmethod
    def handle_route(req: HTTPRequest, res: HTTPResponse):
        nick_name = req.params['nickname'][0]

        if len(nick_name) > 0:
            if not Storage.add_user(nick_name):
                res.send_status(409)
                res.send_response('User exists')
            else:
                res.send_status(200)

                req.cookies['token'] = Token.generate_token_str(nick_name)
                res.send_cookie(req.cookies)
                res.end_headers()
