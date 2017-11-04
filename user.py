from channel import *


class User:
    def __init__(self, username):
        self.__username = username
        self.__current_channel = None
        self.__timestamp = 0

    def get_name(self):
        return self.__username

    def set_channel(self, channel: Channel):
        self.__current_channel = channel

    def get_channel(self):
        return self.__current_channel

    def set_timestamp(self):
        self.__timestamp = time.time()

    def get_timestamp(self):
        return self.__timestamp
