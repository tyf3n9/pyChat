from http.server import BaseHTTPRequestHandler, HTTPServer
from http_controller import *
import urllib.parse as urlparse


class WebServer:

    __PORT_DEFAULT = 80
    __ADDRESS_DEFAULT = '0.0.0.0'

    def __init__(self, port: int =__PORT_DEFAULT, address: str =__ADDRESS_DEFAULT):
        class RequestHandler(BaseHTTPRequestHandler):
            server = None

            def do_GET(self):
                params = {}
                if len(self.path.split('?')) > 1:
                    params = urlparse.parse_qs(self.path.split('?')[1])

                RequestHandler.server.handle_route(self.path.split('?')[0], self, params)

        self.__started = False
        self.__port = port
        self.__routes = {}

        self.__server = HTTPServer((address, port), RequestHandler)
        RequestHandler.server = self

    def start(self):
        if not self.__started:
            self.__started = True
            self.__server.serve_forever()

    def stop(self):
        if self.__started:
            self.__started = False
            self.__server.socket.close()

    def add_route(self, route: str, controller: HTTPController):
        self.__routes[route] = controller

    def handle_route(self, route: str, req_handler: BaseHTTPRequestHandler, params):
        try:
            controller = self.__routes[route]
            if controller is not None:
                controller.handle_route(HTTPRequest(route, params), HTTPResponse(req_handler))
        except KeyError:
            print('No handler for route: ', route)
