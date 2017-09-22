from channel import *


class User:
    def __init__(self, username):
        self.__username = username
        self.__current_channel = None

    def get_name(self):
        return self.__username

    def set_channel(self, channel: Channel):
        self.__current_channel = channel

    def get_channel(self):
        return self.__current_channel
