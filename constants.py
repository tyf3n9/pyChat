class Const:
    KEEP_ALIVE_PERIOD = 30
    ALLOWED_KEEP_ALIVE_MISSES = 1
    KEEP_ALIVE_TIMEOUT = (ALLOWED_KEEP_ALIVE_MISSES + 1) * KEEP_ALIVE_PERIOD
    CLEANUP_TIMEOUT = KEEP_ALIVE_TIMEOUT * 1.1
    DB_PATH = 'storage_db.db'
