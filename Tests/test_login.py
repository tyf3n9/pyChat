import unittest
import requests
import jwt
import _datetime
from Tests.const import *
import subprocess


class TestLogin(unittest.TestCase):
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

    def __del__(self):
        if self.__process is not None:
            self.__process.kill()
            self.__process = None

    def setUp(self):
        self.__process = subprocess.Popen(Const.BACKEND_CMD)
        print(self.__process)

    def tearDown(self):
        if self.__process is not None:
            self.__process.kill()
            self.__process = None

    def verify_tokens(self, cookies: dict, user_name: str):
        token_str = cookies['token']
        token = jwt.decode(str.encode(token_str), self.SECRET, self.ALGO)

        assert token['username'] == user_name
        session_max = _datetime.datetime.utcnow() + _datetime.timedelta(minutes=self.SESSION_TIME)
        assert (session_max.second - token['exp']) < self.TIME_DELTA

        # refresh token
        token_str = cookies['refresh_token']
        token = jwt.decode(str.encode(token_str), self.SECRET, self.ALGO)

        assert token['username'] == user_name
        session_max = _datetime.datetime.utcnow() + _datetime.timedelta(minutes=self.LONG_SESSION_TIME)
        assert (session_max.second - token['exp']) < self.TIME_DELTA

    def test_empty_user(self):
        r = requests.get(Const.LOGIN_URL, {'nickname': ''})
        assert r.status_code == 400

    def test_long_name(self):
        user_name = '3' * 600
        r = requests.get(Const.LOGIN_URL, {'nickname': user_name})

        assert r.status_code == 200
        self.verify_tokens(r.cookies, user_name)

    def test_upper_lower_not_equal(self):
        user1 = 'test'
        user2 = 'TEST'
        r = requests.get(Const.LOGIN_URL, {'nickname': user1})
        p = requests.get(Const.LOGIN_URL, {'nickname': user2})

        self.verify_tokens(r.cookies, user1)
        assert r.status_code == 200

        self.verify_tokens(p.cookies, user2)
        assert p.status_code == 200

    def test_name_combinations(self):
        name_list = [
            '123',
            '!@#$%^&*()-_=+`\'"\\ <>.,/?:;{}[]|',
            'TEST',
            'test',
            'Тест',
            'тест'
        ]

        for name_prefix in name_list:
            user_name = name_prefix
            r = requests.get(Const.LOGIN_URL, {'nickname': user_name})

            assert user_name == user_name and r.status_code == 200
            self.verify_tokens(r.cookies, user_name)

            for name_suffix in name_list:
                user_name = name_prefix + name_suffix
                r = requests.get(Const.LOGIN_URL, {'nickname': user_name})

                assert user_name == user_name and r.status_code == 200
                self.verify_tokens(r.cookies, user_name)

    def test_user_exists(self):
        user_name = 'test1'
        r = requests.get(Const.LOGIN_URL, {'nickname': user_name})
        p = requests.get(Const.LOGIN_URL, {'nickname': user_name})

        self.verify_tokens(r.cookies, user_name)
        assert r.status_code == 200
        assert p.status_code == 409

    def test_no_params(self):
        r = requests.get(Const.LOGIN_URL)
        assert r.status_code == 400


if __name__ == "__main__":
    unittest.main()
