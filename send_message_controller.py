from http_controller import *


class SendMessageController(HTTPController):
    def handle_route(self, req: HTTPRequest, res: HTTPResponse):
        message = req.params['message'][0]
        user = req.mw_data['token']['user_obj']

        channel = user.get_channel()

        if channel is None:
            res.send_status(404)
            res.send_response('Channel not found')
        else:
            channel.add_message(req.mw_data['token']['user_name'], message)
            res.send_status(200)
            res.send_response(message)
