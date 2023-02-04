# Standard lib
import time
from pathlib import Path
from dataclasses import dataclass, field
# Third party
import pandas as pd
# Saif made
from libs.db_manager import DBManager
from appconfig import get_logger

pd.options.display.show_dimensions = True


@dataclass(frozen=True)
class TableConfig:
    """dbテーブル定義

    Attributes
    ----------
    table_name : str
    table_columns : dict
    """
    sqlite_seq: str = "sqlite_sequence"
    token_table: str = "token_meta"
    token_table_cols: dict = field(default_factory=lambda: {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "token": "TEXT NOT NULL",
        "password": "TEXT NOT NULL",
        "date": "TEXT NOT NULL"
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
    """dbとのやり取り操作
    """

    def __init__(self, exe_path: Path):
        """constructor

        Parameters
        ----------
        exe_path: Path
            exeファイルパス
        """
        self.__db_name = "SlackLogAccumulator.db"
        self.__DBMngr = DBManager()
        self.__exe_path = exe_path

        self.__table_config = TableConfig()
        self.__logger = get_logger(__name__)

    def initialize(self, first: bool = False) -> None:
        """初期化の処理

        Parameters
        ----------
        first: bool
            初回起動ならTrue

        Note
        ----------
        token_tableとchannel_tableを作る
        """
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

    def finalize(self) -> None:
        """終了時の処理
        """
        self.__DBMngr.close_connect()

    def get_dbfilename(self) -> str:
        """dbファイルの名前を返す

        Returns
        ----------
        str
            dbファイル名
        """

        return self.__db_name

    def get_dbtable(self) -> list:
        """ログデータテーブルもしくはメンバーマスタのテーブル名のリストを返す

        Returns
        ----------
        list
            dbテーブル名
        """
        ret = self.__DBMngr.get_table_all()
        self.__logger.info(ret)
        exclude_list = [
            self.__table_config.sqlite_seq,
            self.__table_config.token_table,
            self.__table_config.channel_table
        ]

        return [it for it in ret if it not in exclude_list]

    def insert_token(self, token: str, key: str = None) -> None:
        """トークンをdbに登録

        Parameters
        ----------
        token: str
            slack token 文字列
        """
        self.__DBMngr.insert(
            self.__table_config.token_table,
            {
                "token": token,
                "password": key,
                "date": time.strftime('%Y/%m/%d %H:%M:%S')
            }
        )

    def get_token(self) -> list:
        """最新のslack tokenを取得

        Returns
        ----------
        list
            token, key
        """
        ret = self.__DBMngr.select(
            self.__table_config.token_table,
            self.__table_config.token_table_cols.keys()
        )
        print(ret)
        ret["date"] = pd.to_datetime(ret["date"])
        df = ret.loc[ret["date"].idxmax()]
        _, token, password, _ = df.to_list()
        self.__logger.info((token, password))

        return token, password

    def insert_channel(self, chn_id: str, name: str) -> None:
        """チャンネルIDとチャンネル名をdbに登録

        Parameters
        ----------
        chn_id: str
            チャンネルID
        name: str
            チャンネル名
        """
        self.__DBMngr.insert(
            self.__table_config.channel_table,
            {
                "channel_id": chn_id,
                "channel_name": name
            }
        )

    def delete_channel(self, chn_id: str) -> None:
        """dbに登録しているチャンネルを消す

        Parameters
        ----------
        chn_id: str
            チャンネルID
        """
        self.__DBMngr.delete(
            self.__table_config.channel_table,
            "channel_id",
            chn_id
        )

    def get_channel(self) -> pd.DataFrame:
        """dbに登録しているチャンネルを取得する

        Returns
        ----------
        pd.DataFrame
            channel_idとchannel_name
        """
        ret = self.__DBMngr.select(
            self.__table_config.channel_table,
            self.__table_config.channel_table_cols.keys()
        )
        self.__logger.info(ret)

        return ret

    def create_datatable(self, chn_id: str) -> None:
        """ログデータテーブルとメンバーマスタテーブルを作る

        Parameters
        ----------
        chn_id: str
            チャンネルID
        """
        self.__DBMngr.create_table(chn_id, self.__table_config.data_table_cols)
        self.__DBMngr.create_table(
            chn_id + self.__table_config.user_table,
            self.__table_config.user_table_cols
        )

    def insert_member(self, chn_id: str, data: dict) -> None:
        """レコードをreplaceで挿入する

        Parameters
        ----------
        chn_id: str
            チャンネルID
        data: dict
            データのセット
        """
        self.__DBMngr.insert(
            chn_id + self.__table_config.user_table,
            data
        )

    def get_member(self, chn_id: str) -> pd.DataFrame:
        """メンバーマスタからデータを取得する

        Parameters
        ----------
        chn_id: str
            チャンネルID

        Returns
        ----------
        pd.DataFrame
        """
        ret = self.__DBMngr.select(
            chn_id + self.__table_config.user_table,
            self.__table_config.user_table_cols.keys()
        )
        self.__logger.info(ret.head())

        return ret

    def insert_history(self, chn_id: str, data: dict) -> None:
        """レコードをreplaceで挿入する

        Parameters
        ----------
        chn_id: str
            チャンネルID
        data: dict
            データのセット
        """
        self.__DBMngr.insert(chn_id, data)

    def get_history(
            self,
            chn_id: str,
            start: float = None,
            end: float = None
    ) -> pd.DataFrame:
        """ログデータテーブルからデータを取得する

        Parameters
        ----------
        chn_id: str
            チャンネルID
        start: float = None
            start timestamp
        end: float = None
            end timestamp

        Returns
        ----------
        pd.DataFrame
        """
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
