from user import User
from channel import Channel


class Storage:
    __active_users = []
    __channels = [Channel('discovery'),
                  Channel('beauty'),
                  Channel('computers'),
                  Channel('cooking')]

    @staticmethod
    def add_user(username):
        found = False
        for current_user in Storage.__active_users:
            if current_user.get_name() == username:
                found = True

        if not found:
            Storage.__active_users.append( User(username) )

        return not found

    @staticmethod
    def get_channel_list():
        result = []
        for channel in Storage.__channels:
            result.append(channel.get_name())
        return result

    @staticmethod
    def get_user_by_name(username: str):
        for current_user in Storage.__active_users:
            if current_user.get_name() == username:
                return current_user
        return None

    @staticmethod
    def get_channel_by_name(name: str):
        for current_channel in Storage.__channels:
            if current_channel.get_name() == name:
                return current_channel
        return None






