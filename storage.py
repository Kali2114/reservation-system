import sqlite3


class Storage:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.execute("""PRAGMA foreign_keys=ON""")
        self.conn.row_factory = sqlite3.Row
        self.init_schema()

    def init_schema(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            salt BLOB NOT NULL
            )"""
        )

        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS reservations (
            id TEXT PRIMARY KEY,
            user_email TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users(email)
            )"""
        )
        self.conn.commit()
