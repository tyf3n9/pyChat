import unittest
import requests
from Tests.const import *
import subprocess
import jwt
import _datetime


class TestRefreshToken(unittest.TestCase):
    SECRET = 'password'
    ALGO = 'HS256'

    # in minutes
    SESSION_TIME = 3
    LONG_SESSION_TIME = 60

    # in seconds
    TIME_DELTA = 10

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

    def test_successful_refresh(self):
        r = requests.get(Const.REFRESH_TOKEN_URL, cookies=self.cookies)
        assert r.status_code == 200

    def test_unsuccessful_refresh(self):
        r = requests.get(Const.REFRESH_TOKEN_URL)
        assert r.status_code == 401

    def test_expired_refresh_token(self):
        exp_refresh_token = jwt.encode({
                'username': 'testuser',
                'exp': _datetime.datetime.utcnow() - _datetime.timedelta(minutes=10)
            },
            self.SECRET,
            self.ALGO).decode('utf-8')
        r = requests.get(Const.REFRESH_TOKEN_URL, exp_refresh_token)
        assert r.status_code == 401


if __name__ == "__main__":
     unittest.main()

