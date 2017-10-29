import unittest
import requests
from Tests.const import *
import subprocess


class TestChannel(unittest.TestCase):

    URL = 'http://localhost/selectchannel'
    LOGIN_URL = 'http://localhost/login'
    SECRET = 'password'
    ALGO = 'HS256'

    # in minutes
    SESSION_TIME = 3
    LONG_SESSION_TIME = 60

    # in seconds
    TIME_DELTA = 10
    CHANNELS = [
                'discovery',
                'beauty',
                'computers',
                'cooking',
                ]

    def __init__(self, method: str='runTest'):
        super().__init__(methodName=method)
        self.__process = None
        self.cookies = {}

    def __del__(self):
        if self.__process is not None:
            self.__process.kill()
            self.__process = None

    def setUp(self):
        self.__process = subprocess.Popen(Const.BACKEND_CMD)
        r = requests.get(self.LOGIN_URL, {'nickname': 'testuser'})
        self.cookies = dict(r.cookies)

    def tearDown(self):
        if self.__process is not None:
            self.__process.kill()
            self.__process = None

    def test_no_channel(self):
        channel_name = ''
        r = requests.get(self.URL, params={'channel': channel_name}, cookies=self.cookies)

        assert r.status_code == 404

    def test_valid_channel(self):
        channel_name = ''
        for channel_name in self.CHANNELS:
            r = requests.get(self.URL, params={'channel': channel_name}, cookies=self.cookies)
            assert r.status_code == 200

    def test_invalid_channel(self):
        channel_name = "246"
        if channel_name not in self.CHANNELS:
            r = requests.get(self.URL, params={'channel': channel_name}, cookies=self.cookies)
            assert r.status_code == 404

if __name__ == "__main__":
     unittest.main()
