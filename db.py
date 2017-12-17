import sqlite3

from constants import Const

__DB_PATH = Const.DB_PATH


def init_db(db_path: str) -> None:
    global __DB_PATH
    if db_path is not None:
        __DB_PATH = db_path


def read_query(query: str, params: tuple = ()) -> list:
    db = sqlite3.connect(__DB_PATH)
    cursor = db.cursor()
    cursor.execute(query, params)
    result = [row for row in cursor]
    db.close()
    return result


def write_query(query: str, params: tuple = ()) -> None:
    db = sqlite3.connect(__DB_PATH)
    cursor = db.cursor()
    cursor.execute(query, params)
    db.commit()
    db.close()
