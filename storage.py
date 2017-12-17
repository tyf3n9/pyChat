from user import User
from channel import Channel
from db import *
from typing import Optional


class Storage:
    __active_users = []
    __channels = []

    @staticmethod
    def load(db_path) -> None:
        init_db(db_path)

        db_result = read_query('Select Name, ID from Channels')
        Storage.__channels = [Channel(row[0], (row[1])) for row in db_result]

        db_result = read_query('select Users.Name,\
                                Channels.Name, \
                                Channels.ID, \
                                Users.Timestamp from Users left join Channels on Users.Channel = Channels.ID')
        Storage.__active_users = [
            User(
                username=row[0],
                channel=Channel(row[1], row[2]),
                timestamp=row[3]
            ) for row in db_result
        ]

    @staticmethod
    def add_user(username) -> bool:
        found = False
        for current_user in Storage.__active_users:
            if current_user.get_name() == username:
                found = True

        if not found:
            user = User(username)
            Storage.__active_users.append(user)
            user.set_timestamp()
            write_query('INSERT INTO Users(`Name`,`Timestamp`) VALUES(?,?)', (user.get_name(), user.get_timestamp()))

        return not found

    @staticmethod
    def remove_user(user) -> None:
        Storage.__active_users.remove(user)
        write_query('DELETE FROM Users WHERE Name = ?', (user.get_name(),))

    @staticmethod
    def get_all_users() -> list:
        return Storage.__active_users

    @staticmethod
    def get_channel_list() -> list:
        result = []
        for channel in Storage.__channels:
            result.append(channel.get_name())
        return result

    @staticmethod
    def get_user_by_name(username: str) -> Optional[User]:
        for current_user in Storage.__active_users:
            if current_user.get_name() == username:
                return current_user
        return None

    @staticmethod
    def get_channel_by_name(name: str) -> Optional[Channel]:
        for current_channel in Storage.__channels:
            if current_channel.get_name() == name:
                return current_channel
        return None
