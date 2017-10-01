from http.server import BaseHTTPRequestHandler
from http import cookies


class HTTPRequest:
    def __init__(self, uri: str, params: dict, req_handler: BaseHTTPRequestHandler):
        self.uri = uri
        self.params = params
        self.cookies = cookies.SimpleCookie()

        self.mw_data = {}

        cookie_list = req_handler.headers.get_all('Cookie', failobj=[])
        for value in cookie_list:
            self.cookies.load(value)


class HTTPResponse:
    def __init__(self, sender: BaseHTTPRequestHandler):
        self.__sender = sender

    def send_status(self, status: int):
        self.__sender.send_response(status)

    def send_headers(self, headers: str):
        self.__sender.send_header(headers)

    def end_headers(self):
        self.__sender.end_headers()

    def send_cookie(self, cookie: dict):
        items = sorted(cookie.items())
        for key, value in items:
            self.__sender.send_header('Set-Cookie', value.key + '=' + value.value)

    def send_response(self, response: str):
        self.__sender.wfile.write(bytes(response, "utf8"))


class HTTPController:
    @staticmethod
    def handle_route(request: HTTPRequest, response: HTTPResponse):
        print('Default route handler: ', request.uri)
