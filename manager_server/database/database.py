import sqlite3
from typing import Callable
from threading import Lock


class Database:
    def __init__(self, name: str):
        self.lock = Lock()
        self.database = sqlite3.connect(name, check_same_thread=False)

        # setting-up database if not setup already
        cursor = self.database.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS accounts(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS passwords(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, owner INTEGER NOT NULL, website TEXT, username TEXT, PASSWORD TEXT)")
        self.database.commit()

    # allows for multithread access to database
    def enter_db_context(self, context: Callable[[sqlite3.Connection], any]) -> any:
        with self.lock:
            return context(self.database)
