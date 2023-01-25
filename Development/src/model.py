# Standard lib
import time
from pathlib import Path
from dataclasses import dataclass, field
# Saif made
from libs.DB_manager import DBManager


@dataclass(frozen=True)
class TableConfig:
    token_table: str = "token_meta"
    token_table_cols: dict = field(default_factory=lambda: {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "token": "STRING NOT NULL",
        "date": "STRING"
    })
    channel_table: str = "channel_master"
    channel_table_cols: dict = field(default_factory=lambda: {
        "channel_id": "STRING PRIMARY KEY",
        "channel_name": "STRING NOT NULL",
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
                self.__table_config.token_table,
                self.__table_config.token_table_cols
            )
            self.__DBMngr.create_table(
                self.__cursor,
                self.__table_config.channel_table,
                self.__table_config.channel_table_cols
            )

    def get_dbfilename(self):

        return self.__db_name

    def get_dbtable(self):

        ret = self.__DBMngr.get_table_all(self.__cursor)

        return ret

    def insert_token(self, token: str):

        self.__DBMngr.insert(
            self.__cursor,
            self.__table_config.token_table,
            {
                "token": token,
                "date": time.strftime('%Y/%m/%d %H:%M:%S')
            }
        )

    def get_token(self) -> str:

        token_data = self.__DBMngr.select(
            self.__cursor,
            self.__table_config.token_table,
            self.__table_config.token_table_cols.keys()
        )

        return token_data[-1].get("token")

    def insert_channel(self, name: str, chn_id: str):

        self.__DBMngr.insert(
            self.__cursor,
            self.__table_config.channel_table,
            {
                "channel_id": chn_id,
                "channel_name": name
            }
        )

    def get_channel(self) -> list:

        channel_data = self.__DBMngr.select(
            self.__cursor,
            self.__table_config.channel_table,
            self.__table_config.channel_table_cols.keys()
        )

        return channel_data
