# Standard lib
import time
from pathlib import Path
from dataclasses import dataclass, field
# Saif made
from libs.DB_manager import DBManager


@dataclass(frozen=True)
class TableConfig:
    token_store: dict = field(default_factory=lambda: {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "token": "TEXT NOT NULL",
        "date": "TEXT"
    })


class Model():

    def __init__(self, exe_path: Path) -> None:

        self.__db_name = "SlackLogAccumulator.db"
        self.__DBMngr = DBManager()
        self.__exe_path = exe_path
        self.__cursor = None
        self.__table_config = TableConfig()

    def initialize(self, first: bool):

        self.__cursor = self.__DBMngr.initialize(
            self.__exe_path / self.__db_name
        )
        if first:
            self.__DBMngr.create_table(
                self.__cursor,
                "TOKEN_STORE",
                self.__table_config.token_store
            )

    def get_dbfilename(self):

        return self.__db_name

    def get_dbtable(self):

        return self.__DBMngr.get_table_all(self.__cursor)

    def insert_token(self, token: str):

        self.__DBMngr.insert(
            self.__cursor,
            "TOKEN_STORE",
            {
                "token": token,
                "date": time.strftime('%Y/%m/%d %H:%M:%S')
            }
        )

    def get_token(self):

        token_data = self.__DBMngr.select(
            self.__cursor,
            "TOKEN_STORE",
            self.__table_config.token_store.keys()
        )

        return token_data[-1].get("token")
