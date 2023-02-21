import sqlite3
from manager_server.database.database import Database


class Password:
    id: int
    owner: int
    username: str
    password: str
    website: str

    def __init__(self, id: int, owner: int, username: str, password: str, website: str):
        self.id = id
        self.owner = owner
        self.username = username
        self.password = password
        self.website = website

    def insert_inner(self, connection: sqlite3.Connection):
        cursor = connection.cursor()
        self.id = cursor.execute("INSERT INTO passwords(owner, username, password, website) VALUES(?, ?, ?, ?) RETURNING id",
                                 (self.owner, self.username, self.password, self.website)).fetchone()[0]
        connection.commit()

    def insert(self, database: Database):
        database.enter_db_context(lambda e: self.insert_inner(e))

    def delete_inner(self, connection: sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM passwords WHERE id=? AND owner=?", (self.id, self.owner))
        connection.commit()

    def delete(self, database: Database):
        database.enter_db_context(lambda e: self.delete_inner(e))

    def delete_all_inner(self, connection: sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM passwords WHERE owner=?", (self.owner,))
        connection.commit()

    def delete_all(self, database: Database):
        database.enter_db_context(lambda e: self.delete_all_inner(e))

    def get_passwords_inner(owner: int, connection: sqlite3.Connection):
        cursor = connection.cursor()

        results = list(map(lambda e: Password(e[0], owner, e[1], e[2], e[3]), \
                      cursor
                      .execute(
                          "SELECT id, username, password, website FROM passwords WHERE owner=? ORDER BY username",
                          (owner,)
                      )
                      .fetchall()))

        return results

    def get_passwords(owner: int, database: Database):
        return database.enter_db_context(lambda e: Password.get_passwords_inner(owner, e))
