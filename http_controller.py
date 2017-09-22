from http.server import BaseHTTPRequestHandler


class HTTPRequest:
    def __init__(self, uri, params):
        self.uri = uri
        self.params = params


class HTTPResponse:
    def __init__(self, sender: BaseHTTPRequestHandler):
        self.__sender = sender

    def send_status(self, status: int):
        self.__sender.send_response(status)

    def send_headers(self, headers: list):
        self.__sender.send_header('Content-type', 'text/plain; charset=utf-8')
        self.__sender.end_headers()

    def send_response(self, response: str):
        self.__sender.wfile.write(bytes(response, "utf8"))


class HTTPController:
    @staticmethod
    def handle_route(request: HTTPRequest, response: HTTPResponse):
        print('Default route handler: ', request.uri)
