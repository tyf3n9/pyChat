import time


class Message:
    def __init__(self, text) -> None:
        self.__id = time.time()
        self.__message_text = text

    def get_message(self) -> str:
        return self.__message_text

    def get_id(self) -> int:
        return self.__id
