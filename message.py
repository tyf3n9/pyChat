import time


class Message:
    def __init__(self, text):
        self.__id = time.time()
        self.__message_text = text

    def get_message(self):
        return self.__message_text


