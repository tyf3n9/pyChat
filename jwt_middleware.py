from web_server import WebMiddleware
from http_controller import *
from api_token import *
from storage import *


class JwtMiddleWare(WebMiddleware):
    def handle_request(self, req: HTTPRequest, res: HTTPResponse):
        result = True
        try:
            token = Token(req.cookies['token'].value)
            user_name = token.extract_user_name()
            user = Storage.get_user_by_name(user_name)

            if token.is_valid():
                if user is None:
                    Storage.add_user(user_name)
                    user = Storage.get_user_by_name(user_name)

                req.mw_data['token'] = {'user_name': user_name, 'user_obj': user}
                res.send_status(200)
            else:
                result = False
        except KeyError:
            result = False

        if not result:
            res.send_status(403)
            res.end_headers()
        return result
