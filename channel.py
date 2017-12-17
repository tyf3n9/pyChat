from message import *
from db import *
import time


class Channel:
    def __init__(self, name, channel_id) -> None:
        self.__name = name
        self.__id = channel_id
        self.__messages_list = []
        self.__messages_list = read_query('Select Text from Messages WHERE Channel = ?', (channel_id,))

    def get_name(self) -> str:
        return self.__name

    def get_channel_id(self) -> int:
        return self.__id

    def add_message(self, username, text) -> None:
        message = Message(username+': '+text)
        self.__messages_list.append(message)

        write_query('INSERT INTO Messages(`Channel`,`Timestamp`,`Text`) VALUES(?,?,?)', (self.__id, time.time(), text))

    def get_messages(self) -> list:
        text_list = []
        for current_message in self.__messages_list:
            text_list.append(current_message.get_message())
        return text_list
