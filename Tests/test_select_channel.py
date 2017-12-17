import unittest

import os
import requests
import shutil

from Tests.const import *
import subprocess


class TestChannel(unittest.TestCase):
    SECRET = 'password'
    ALGO = 'HS256'

    # in minutes
    SESSION_TIME = 3
    LONG_SESSION_TIME = 60

    # in seconds
    TIME_DELTA = 10
    CHANNELS = ['discovery',
                'beauty',
                'computers',
                'cooking'
                ]

    def __init__(self, method: str='runTest') -> None:
        super().__init__(methodName=method)
        self.__process = None
        self.cookies = {}

    def __del__(self) -> None:
        if self.__process is not None:
            self.__process.kill()
            self.__process = None

    def setUp(self) -> None:
        shutil.copy2('./empty_test_db.db', './empty_test_db_copy.db')

        self.__process = subprocess.Popen(Const.BACKEND_CMD + ' ' + Const.DB_PATH)
        r = requests.get(Const.LOGIN_URL, {'nickname': 'testuser'})
        self.cookies = dict(r.cookies)

    def tearDown(self) -> None:
        if self.__process is not None:
            self.__process.kill()
            self.__process = None
        os.remove("./empty_test_db_copy.db")

    def test_no_channel(self) -> None:
        channel_name = ''
        r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': channel_name}, cookies=self.cookies)

        assert r.status_code == 404

    def test_valid_channel(self) -> None:
        for channel_name in self.CHANNELS:
            r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': channel_name}, cookies=self.cookies)
            assert channel_name == channel_name and r.status_code == 200

    def test_invalid_channel(self) -> None:
        channel_name = "246"
        if channel_name not in self.CHANNELS:
            r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': channel_name}, cookies=self.cookies)
            assert r.status_code == 404

if __name__ == "__main__":
    unittest.main()
