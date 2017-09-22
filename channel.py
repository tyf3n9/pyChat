from message import *


class Channel:
    def __init__(self, name):
        self.__name = name
        self.__messages_list = []

    def get_name(self):
        return self.__name

    def add_message(self, username, text):
        message = Message(username+': '+text)
        self.__messages_list.append(message)

    def get_messages(self):
        text_list = []
        for current_message in self.__messages_list:
            text_list.append(current_message.get_message())
        return text_list




