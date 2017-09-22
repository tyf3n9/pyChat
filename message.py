import datetime


class Message:
    def __init__(self, text):
        self.__id = datetime.datetime.now()
        self.__message_text = text

    def get_message(self):
        return self.__message_text


