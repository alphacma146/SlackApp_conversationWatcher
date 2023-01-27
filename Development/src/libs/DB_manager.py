# Standard lib
from sqlite3 import Cursor
import sqlite3
from pathlib import Path
# Third party
import pandas as pd
# Self made
from .abst_db import IDBManager


class DBManager(IDBManager):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "__instance"):
            cls.__instance = super(DBManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.__connect = None
        self.__cursor = None

    def initialize(self, db_path: Path) -> Cursor:
        self.__connect = sqlite3.connect(db_path)
        self.__cursor = self.__connect.cursor()

    def query_execute(
            self,
            sql_text: str,
            values: tuple = None
    ) -> None:

        if values is None:
            self.__cursor.execute(sql_text)
        else:
            self.__cursor.execute(sql_text, values)
        self.__connect.commit()

    def get_table_all(self, ) -> list:

        query = "SELECT * FROM sqlite_master WHERE type='table'"
        self.query_execute(self.__cursor, query)

        return self.__cursor.fetchall()

    def create_table(
        self,
        table_name: str,
        columns: dict[str, str]
    ):

        col = ", ".join([f"{key} {val}" for (key, val) in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({col})"
        self.query_execute(query)

    def remove_table(self, table_name: str):

        self.query_execute(f"DROP TABLE {table_name}")

    def insert(self, table_name: str, data: dict):

        col = ", ".join(data.keys())
        sac = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name}({col}) values({sac})"
        self.query_execute(query, values=tuple(data.values()))

    def select(
        self,
        table_name: str,
        columns: list,
        terms: str = None
    ) -> dict:

        col = ", ".join(columns)
        if terms is None:
            query = f"SELECT {col} FROM {table_name}"
        else:
            query = f"SELECT {col} FROM {table_name} WHERE {terms}"

        # DBからの戻り値は[(data,data,data),(...)]のため
        ret = pd.read_sql_query(query, self.__connect)

        return ret

    def close_connect(self) -> None:

        self.__connect.close()
