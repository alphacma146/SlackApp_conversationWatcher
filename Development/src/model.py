# Standard lib
import time
from pathlib import Path
from dataclasses import dataclass, field
# Third party
import pandas as pd
# Saif made
from libs.DB_manager import DBManager
from appconfig import get_logger, MessageText

pd.options.display.show_dimensions = True


@dataclass(frozen=True)
class TableConfig:
    sqlite_seq: str = "sqlite_sequence"
    token_table: str = "token_meta"
    token_table_cols: dict = field(default_factory=lambda: {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "token": "TEXT NOT NULL",
        "date": "TEXT"
    })
    channel_table: str = "channel_master"
    channel_table_cols: dict = field(default_factory=lambda: {
        "channel_id": "TEXT PRIMARY KEY",
        "channel_name": "TEXT NOT NULL",
    })
    user_table: str = "_user_master"
    user_table_cols: dict = field(default_factory=lambda: {
        "user_id": "TEXT PRIMARY KEY",
        "user_name": "TEXT NOT NULL",
        "real_name": "TEXT",
    })
    data_table_cols: dict = field(default_factory=lambda: {
        "id": "TEXT PRIMARY KEY",
        "user_id": "TEXT NOT NULL",
        "timestamp": "TEXT NOT NULL",
        "text": "TEXT NOT NULL",
        "reaction": "INT"
    })


class Model():

    def __init__(self, exe_path: Path) -> None:

        self.__db_name = "SlackLogAccumulator.db"
        self.__DBMngr = DBManager()
        self.__exe_path = exe_path

        self.__table_config = TableConfig()
        self.__logger = get_logger(__name__)

    def initialize(self, first: bool):

        self.__DBMngr.initialize(self.__exe_path / self.__db_name)
        if first:
            self.__DBMngr.create_table(
                self.__table_config.token_table,
                self.__table_config.token_table_cols
            )
            self.__DBMngr.create_table(
                self.__table_config.channel_table,
                self.__table_config.channel_table_cols
            )

    def get_dbfilename(self):

        return self.__db_name

    def get_dbtable(self) -> list:

        ret = self.__DBMngr.get_table_all()
        self.__logger.info(ret)
        exclude_list = [
            self.__table_config.sqlite_seq,
            self.__table_config.token_table,
            self.__table_config.channel_table
        ]

        return [it for it in ret if it not in exclude_list]

    def insert_token(self, token: str):

        self.__DBMngr.insert(
            self.__table_config.token_table,
            {
                "token": token,
                "date": time.strftime('%Y/%m/%d %H:%M:%S')
            }
        )

    def get_token(self) -> str:

        ret = self.__DBMngr.select(
            self.__table_config.token_table,
            self.__table_config.token_table_cols.keys()
        )
        self.__logger.info(ret)
        ret["date"] = pd.to_datetime(ret["date"])
        df = ret.loc[[ret["date"].idxmax()]]
        token = df["token"].to_string(index=False)

        return token

    def insert_channel(self, chn_id: str, name: str):

        self.__DBMngr.insert(
            self.__table_config.channel_table,
            {
                "channel_id": chn_id,
                "channel_name": name
            }
        )

    def delete_channel(self, chn_id: str):

        self.__DBMngr.delete(
            self.__table_config.channel_table,
            "channel_id",
            chn_id
        )

    def get_channel(self) -> list:

        ret = self.__DBMngr.select(
            self.__table_config.channel_table,
            self.__table_config.channel_table_cols.keys()
        )
        self.__logger.info(ret)

        return ret

    def create_datatable(self, chn_id: str):

        self.__DBMngr.create_table(chn_id, self.__table_config.data_table_cols)
        self.__DBMngr.create_table(
            chn_id + self.__table_config.user_table,
            self.__table_config.user_table_cols
        )

    def insert_member(self, chn_id: str, data: dict):

        self.__DBMngr.insert(
            chn_id + self.__table_config.user_table,
            data
        )

    def insert_history(self, chn_id: str, data: dict):

        self.__DBMngr.insert(chn_id, data)

    def get_member(self, chn_id: str) -> pd.DataFrame:

        ret = self.__DBMngr.select(
            chn_id + self.__table_config.user_table,
            self.__table_config.user_table_cols.keys()
        )
        self.__logger.info(ret.head())

        return ret

    def get_history(self, chn_id: str, start=None, end=None) -> pd.DataFrame:

        match (start, end):
            case (None, None):
                tern = None
            case (_, None):
                tern = f"timestamp >= {start}"
            case (None, _):
                tern = f"timestamp <= {end}"
            case _:
                tern = f"timestamp BETWEEN {start} AND {end}"

        ret = self.__DBMngr.select(
            chn_id,
            self.__table_config.data_table_cols.keys(),
            tern
        )
        self.__logger.info(ret.head())

        return ret
