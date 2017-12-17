import unittest

import os
import requests
import shutil

from Tests.const import *
import subprocess


class TestKeepAlive(unittest.TestCase):
    SECRET = 'password'
    ALGO = 'HS256'

    # in minutes
    SESSION_TIME = 3
    LONG_SESSION_TIME = 60

    # in seconds
    TIME_DELTA = 10

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

    def test_successful_keep_alive(self) -> None:
        r = requests.get(Const.KEEP_ALIVE_URL, cookies=self.cookies)
        assert r.status_code == 200
