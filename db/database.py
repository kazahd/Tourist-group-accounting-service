import sqlite3

DB_PATH = "data/tourist.sqlite"


def get_connection():
    """Создает соединение с БД и включает проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
