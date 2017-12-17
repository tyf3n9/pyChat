from storage import *
from constants import *
import time


def clean_up() -> None:
    active_users = Storage.get_all_users()
    print('List of active users:', len(active_users))
    for current_user in active_users:
        time_stamp = current_user.get_timestamp()
        if(time.time() - time_stamp) > Const.KEEP_ALIVE_TIMEOUT:
            print('timestamp', (time.time() - time_stamp))
            print('Timeout:', Const.KEEP_ALIVE_TIMEOUT)
            Storage.remove_user(current_user)
            print('Deleted Username:', current_user.get_name())
