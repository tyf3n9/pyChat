from web_server import WebMiddleware
from http_controller import *
from api_token import *
from storage import *


class JwtMiddleWare(WebMiddleware):
    def handle_request(self, req: HTTPRequest, res: HTTPResponse):
        try:
            token = Token(req.cookies['token'].value)
            user_name = token.extract_user_name()
            user = Storage.get_user_by_name(user_name)

            if user is not None:
                req.mw_data['token'] = {'user_name': user_name, 'user_obj': user}
                result = token.is_valid()
            else:
                result = False
        except KeyError:
            result = False

        if not result:
            res.send_status(403)
            res.send_response('Token expired')

        return result