from http_controller import *


class SendMessageController(HTTPController):
    def handle_route(self, req: HTTPRequest, res: HTTPResponse) -> None:
        try:
            message = req.params['message'][0]
            if len(message) > 0:
                user = req.mw_data['token']['user_obj']

                channel = user.get_channel()

                if channel is None:
                    res.send_status(404)
                    res.end_headers()
                else:
                    channel.add_message(req.mw_data['token']['user_name'], message)
                    res.send_status(200)
                    res.end_headers()
                    res.send_response(message)
            else:
                res.send_status(404)
                res.end_headers()
        except KeyError:
            res.send_status(404)
            res.end_headers()
