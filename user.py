from typing import Optional

from channel import *
from db import *


class User:
    def __init__(self, username: str, channel: Channel = None, timestamp: int = 0) -> None:
        self.__username = username
        self.__current_channel = channel
        if timestamp is None:
            self.__timestamp = 0
        else:
            self.__timestamp = timestamp

    def get_name(self) -> str:
        return self.__username

    def set_channel(self, channel: Channel) -> None:
        self.__current_channel = channel
        write_query('Update Users SET Channel = ? Where Name = ?', (channel.get_channel_id(), User.get_name(self)))

    def get_channel(self) -> Optional[Channel]:
        return self.__current_channel

    def set_timestamp(self) -> None:
        self.__timestamp = time.time()

    def get_timestamp(self) -> int:
        return self.__timestamp
