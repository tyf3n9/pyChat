from http.server import BaseHTTPRequestHandler
from http import cookies
from abc import *


class HTTPRequest:
    def __init__(self, uri: str, params: dict, req_handler: BaseHTTPRequestHandler) -> None:
        self.uri = uri
        self.params = params
        self.cookies = cookies.SimpleCookie()

        self.mw_data = {}

        cookie_list = req_handler.headers.get_all('Cookie', failobj=[])
        for value in cookie_list:
            self.cookies.load(value)


class HTTPResponse:
    def __init__(self, sender: BaseHTTPRequestHandler) -> None:
        self.__sender = sender

    def send_status(self, status: int) -> None:
        self.__sender.send_response(status)

    def send_headers(self, headers: str) -> None:
        self.__sender.send_header(headers)

    def end_headers(self) -> None:
        self.__sender.end_headers()

    def send_cookie(self, cookie: dict) -> None:
        items = sorted(cookie.items())
        for key, value in items:
            self.__sender.send_header('Set-Cookie', value.key + '=' + value.value)

    def send_response(self, response: str) -> None:
        self.__sender.wfile.write(bytes(response, "utf8"))


class HTTPController:
    @abstractmethod
    def handle_route(self, request: HTTPRequest, response: HTTPResponse) -> None:
        pass
