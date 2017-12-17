import unittest
import os
import requests
import shutil

from Tests.const import *
import subprocess
import json


class TestCheckMessages(unittest.TestCase):
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

    def get_first_message(self) -> None:
        result = ""
        r = requests.get(Const.CHECK_MESSAGES_URL, cookies=self.cookies)
        try:
            messages_list = json.loads(r.text)
            if len(messages_list) > 0:
                result = messages_list[0]
                assert r.status_code == 200
            else:
                assert r.status_code == 200
        except json.JSONDecodeError:
            assert r.status_code == 400

        return result

    def get_first_channel(self) -> None:
        result = ""
        r = requests.get(Const.LIST_CHANNELS_URL, cookies=self.cookies)
        try:
            channel_list = json.loads(r.text)
            if len(channel_list) > 0:
                result = channel_list[0]
                assert r.status_code == 200
            else:
                assert r.status_code == 200
        except json.JSONDecodeError:
            assert r.status_code == 400

        return result

    def send_message_to_first_channel(self) -> None:
        message = 'Happy Birthday'

        r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': self.get_first_channel()}, cookies=self.cookies)
        assert r.status_code == 200
        r = requests.get(Const.SEND_MESSAGE_URL, params={'message': message}, cookies=self.cookies)
        assert r.status_code == 200
        r = requests.get(Const.CHECK_MESSAGES_URL, cookies=self.cookies)
        print("Test:",  (json.loads(r.text)))
        assert r.status_code == 200

    def check_message_on_first_channel(self) -> None:
        r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': self.get_first_channel()}, cookies=self.cookies)
        assert r.status_code == 200

        r = requests.get(Const.CHECK_MESSAGES_URL, cookies=self.cookies)
        message_array = json.loads(r.text)
        assert not message_array == [] and r.status_code == 200

    def check_no_messages_on_channel(self, channel_name) -> None:
        r = requests.get(Const.SELECT_CHANNEL_URL, params={'channel': channel_name},
                         cookies=self.cookies)
        assert r.status_code == 200

        r = requests.get(Const.CHECK_MESSAGES_URL, cookies=self.cookies)
        message_array = json.loads(r.text)
        assert message_array == [] and r.status_code == 200

    def test_valid_message(self) -> None:
        self.send_message_to_first_channel()

    def test_none_channel_selected(self) -> None:
        message = 'No channel'

        r = requests.get(Const.SEND_MESSAGE_URL, params={'message': message}, cookies=self.cookies)
        assert r.status_code == 404
        r = requests.get(Const.CHECK_MESSAGES_URL, cookies=self.cookies)
        assert r.status_code == 404

    def test_no_messages_on_each_channel(self) -> None:
        r = requests.get(Const.LIST_CHANNELS_URL, cookies=self.cookies)
        assert r.status_code == 200
        try:
            channel_list = json.loads(r.text)
            assert len(channel_list) > 0
            for channel_name in channel_list:
                self.check_no_messages_on_channel(channel_name)
        except json.JSONDecodeError:
            assert not "Failed to decode channel list"

    def test_message_on_first_channel(self) -> None:
        r = requests.get(Const.LIST_CHANNELS_URL, cookies=self.cookies)
        assert r.status_code == 200
        try:
            channel_list = json.loads(r.text)
            assert len(channel_list) >= 0
            for channel_name in channel_list:
                if channel_name == channel_list[0]:

                    self.send_message_to_first_channel()
                else:
                    # particular user gets empty list of messages on others channels
                    self.check_no_messages_on_channel(channel_name)
            self.check_message_on_first_channel()
        except json.JSONDecodeError:
            assert not "Failed to decode channel list"

if __name__ == "__main__":
    unittest.main()
