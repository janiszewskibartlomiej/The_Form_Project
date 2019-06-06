import sqlite3


def polaczenie():
    conn = sqlite3.connect('questionDataBase.db')
    conn.row_factory = sqlite3.Row
    return conn
