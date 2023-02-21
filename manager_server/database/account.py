import sqlite3
from enum import Enum
from manager_server.database.database import Database


class AccountCreationResult(Enum):
    OK = 0
    EXISTS = 1


class Account:
    id: int
    username: str
    password: str

    def __init__(self, id: int, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password

    def insert_inner(self, connection: sqlite3.Connection) -> AccountCreationResult:
        cursor = connection.cursor()
        res = cursor.execute("SELECT id FROM accounts WHERE username=?", (self.username,))
        if res.fetchone() is not None:
            return AccountCreationResult.EXISTS

        self.id = cursor.execute("INSERT INTO accounts(username, password) VALUES(?, ?) RETURNING id",
                                 (self.username, self.password)).fetchone()[0]
        connection.commit()
        return AccountCreationResult.OK

    def insert(self, database: Database) -> AccountCreationResult:
        return database.enter_db_context(lambda e: self.insert_inner(e))

    def delete_inner(self, connection: sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM accounts WHERE id=?", (self.id,))
        connection.commit()

    def delete(self, database: Database):
        database.enter_db_context(lambda e: self.delete_inner(e))

    def find_inner(connection: sqlite3.Connection, username: str):
        cursor = connection.cursor()
        res = cursor.execute("SELECT id, username, password FROM accounts WHERE username=?", (username,))
        existing = res.fetchone()
        if existing is None:
            return None

        connection.commit()

        return Account(existing[0], existing[1], existing[2])

    def find(database: Database, username: str):
        return database.enter_db_context(lambda e: Account.find_inner(e, username))
