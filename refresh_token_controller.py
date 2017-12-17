from http_controller import *
from api_token import *


class RefreshTokenController(HTTPController):
    def handle_route(self, req: HTTPRequest, res: HTTPResponse) -> None:
        try:
            token = Token(req.cookies['refresh_token'].value)
            user_name = token.extract_user_name()

            if token.is_valid():
                res.send_status(200)
                req.cookies['token'] = Token.generate_token_str(user_name, Token.SESSION_TIME)
                req.cookies['refresh_token'] = Token.generate_token_str(user_name, Token.LONG_SESSION_TIME)
                res.send_cookie(req.cookies)
                res.end_headers()
        except KeyError:
                res.send_status(401)    # sent response('Not authorised')
                res.end_headers()
