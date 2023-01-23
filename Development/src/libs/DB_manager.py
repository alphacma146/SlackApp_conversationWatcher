# Standard lib
from sqlite3 import Cursor
import sqlite3
from pathlib import Path
# Self made
from .abst_db import IDBManager


class DBManager(IDBManager):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "__instance"):
            cls.__instance = super(DBManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.__connect = None

    def initialize(self, db_path: Path) -> Cursor:
        self.__connect = sqlite3.connect(db_path)

        return self.__connect.cursor()

    def query_execute(
            self,
            cursor: Cursor,
            sql_text: str,
            values: tuple = None
    ) -> None:

        cursor.execute(sql_text, values)
        self.__connect.commit()

    def get_table_all(self, cursor: Cursor) -> list:

        query = "SELECT * FROM sqlite_master WHERE type='table'"
        self.query_execute(cursor, query)

        return cursor.fetchall()

    def create_table(
        self,
        cursor: Cursor,
        table_name: str,
        columns: dict[str, str]
    ):

        col = ", ".join([f"{key} {val}" for (key, val) in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name}({col})"
        self.query_execute(cursor, query)

    def remove_table(self, cursor: Cursor, table_name: str):

        self.query_execute(cursor, f"DROP TABLE {table_name}")

    def insert(self, cursor: Cursor, table_name: str, data: dict):

        col = ", ".join(data.keys())
        sac = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name}({col}) values({sac})"
        self.query_execute(cursor, query, values=data.values())

    def select(
        self,
        cursor: Cursor,
        table_name: str,
        columns: list,
        terms: str
    ):

        col = ", ".join(columns)
        query = f"SELECT {col} FORM {table_name} {terms}"
        self.query_execute(cursor, query)

        return cursor.fetchall()

    def close_connect(self) -> None:

        self.__connect.close()
