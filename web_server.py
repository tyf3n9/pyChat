from http.server import BaseHTTPRequestHandler, HTTPServer
from http_controller import *
import urllib.parse as urlparse
from typing import *


class WebMiddleware:
    def handle_request(self, req: HTTPRequest, res: HTTPResponse):
        return True


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
        self.__middle_wares = []

        self.__server = HTTPServer((address, port), RequestHandler)
        RequestHandler.server = self

    def register_mw(self, mw: Type[WebMiddleware]):
        self.__middle_wares.append(mw())

    def start(self):
        if not self.__started:
            self.__started = True
            self.__server.serve_forever()

    def stop(self):
        if self.__started:
            self.__started = False
            self.__server.socket.close()

    def add_route(self, route: str, controller: Type[HTTPController], ignored_mws: List[Type[WebMiddleware]] = []):
        self.__routes[route] = {'controller': controller, 'ignored_mws': ignored_mws}

    def handle_route(self, route: str, req_handler: BaseHTTPRequestHandler, params):
        try:
            controller = self.__routes[route]['controller']
            ignored_mws = self.__routes[route]['ignored_mws']
            if controller is not None:
                req = HTTPRequest(route, params, req_handler)
                res = HTTPResponse(req_handler)

                # call middleware
                for mw in self.__middle_wares:
                    if (type(mw) not in ignored_mws) and (not mw.handle_request(req, res)):
                        return

                controller().handle_route(req, res)
        except KeyError:
            print('No handler for route: ', route)
