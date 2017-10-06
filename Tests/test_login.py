import unittest
import requests
import jwt
import _datetime


class TestLogin(unittest.TestCase):
    URL = 'http://localhost/login'
    SECRET = 'password'
    ALGO = 'HS256'

    # in minutes
    SESSION_TIME = 3
    LONG_SESSION_TIME = 60

    # in seconds
    TIME_DELTA = 10

    def test_empty_user(self):
        r = requests.get(self.URL, {'nickname': ''})
        assert r.status_code == 400

    def test_valid_user(self):
        r = requests.get(TestLogin.URL, {'nickname': 'test1'})
        assert r.status_code == 200

        # access token
        token_str = r.cookies['token']
        token = jwt.decode(str.encode(token_str), self.SECRET, self.ALGO)

        assert token['username'] == 'test1'
        session_max = _datetime.datetime.utcnow() + _datetime.timedelta(minutes=self.SESSION_TIME)
        assert (session_max.second - token['exp']) < self.TIME_DELTA

        # refresh token
        token_str = r.cookies['refresh_token']
        token = jwt.decode(str.encode(token_str), self.SECRET, self.ALGO)

        assert token['username'] == 'test1'
        session_max = _datetime.datetime.utcnow() + _datetime.timedelta(minutes=self.LONG_SESSION_TIME)
        assert (session_max.second - token['exp']) < self.TIME_DELTA


if __name__ == "__main__":
    unittest.main()
