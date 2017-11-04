import requests
from Tests.const import *
import subprocess
import unittest
import json


class TestSendMessage(unittest.TestCase):
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
                'cooking']

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
        r = requests.get(Const.LOGIN_URL, {'nickname': 'testuser'})
        self.cookies = dict(r.cookies)

    def tearDown(self):
        if self.__process is not None:
            self.__process.kill()
            self.__process = None

    def get_first_channel(self):
        result = ""
        r = requests.get(Const.LIST_CHANNELS_URL, cookies=self.cookies)
        assert r.status_code == 200
        try:
            channel_list = json.loads(r.text)
            if len(channel_list) > 0:
                result = channel_list[0]
        except json.JSONDecodeError:
            assert r.status_code == 400

        return result

    def test_valid_message(self):
        message = 'HELLo'

        r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': self.get_first_channel()}, cookies=self.cookies)
        assert r.status_code == 200
        r = requests.get(Const.SEND_MESSAGE_URL, params={'message': message}, cookies=self.cookies)
        assert r.status_code == 200

    def test_send_empty_message(self):
        message = ""
        r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': self.get_first_channel()}, cookies=self.cookies)
        assert r.status_code == 200
        r = requests.get(Const.SEND_MESSAGE_URL, params={'message': message}, cookies=self.cookies)
        assert r.status_code == 404

    def test_send_message_to_no_channel(self):  # user doesn't select any chanel and try to send message
        message = "No channel selected"

        r = requests.get(Const.SEND_MESSAGE_URL, params={'message': message}, cookies=self.cookies)
        assert r.status_code == 404

    def test_no_cookies(self):     # user not authorised and try to send message
        message = "no cookies"
        r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': self.get_first_channel()})
        assert r.status_code == 403
        r = requests.get(Const.SEND_MESSAGE_URL, params={'message': message}, cookies=self.cookies)
        assert r.status_code == 404

    def test_send_long_message(self):
        message = 'test' * 600
        r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': self.get_first_channel()}, cookies=self.cookies)
        assert r.status_code == 200
        r = requests.get(Const.SEND_MESSAGE_URL, params={'message': message}, cookies=self.cookies)
        assert r.status_code == 200

if __name__ == "__main__":
    unittest.main()
