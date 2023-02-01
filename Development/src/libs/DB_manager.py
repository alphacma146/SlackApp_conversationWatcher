# Standard lib
import sqlite3
from pathlib import Path
# Third party
import pandas as pd
# Self made
from .abst_db import IDBManager

pd.set_option("display.max_colwidth", None)


class DBManager(IDBManager):
    """dbを管理する
    """
    def __new__(cls, *args, **kargs):
        """constructor

        Note
        ----------
        Singleton
        """
        if not hasattr(cls, "__instance"):
            cls.__instance = super(DBManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        """constructor
        """
        self.__connect = None
        self.__cursor = None

    def initialize(self, db_path: Path) -> None:
        """dbを初期化する

        Parameters
        ----------
        db_path: Path
            dbのパス
        """
        self.__connect = sqlite3.connect(db_path, check_same_thread=False)
        self.__cursor = self.__connect.cursor()

    def query_execute(
            self,
            sql_text: str,
            values: tuple = None
    ) -> None:
        """クエリを発行する

        Parameters
        ----------
        sql_text: str
            クエリ文
        values: tuple = None
            insertならその値
        """
        if values is None:
            self.__cursor.execute(sql_text)
        else:
            self.__cursor.execute(sql_text, values)
        self.__connect.commit()

    def get_table_all(self) -> list:
        """持っているテーブル名すべて返す

        Returns
        ----------
        list
            dbテーブル名
        """
        query = "SELECT * FROM sqlite_master WHERE type='table'"
        self.query_execute(query)

        return [name for (_, name, _, _, _) in self.__cursor.fetchall()]

    def create_table(
        self,
        table_name: str,
        columns: dict[str, str]
    ):
        """テーブルを作る

        Parameters
        ----------
        table_name: str
            テーブル名
        columns: dict[str, str]
            columnの定義
        """
        col = ", ".join([f"{key} {val}" for (key, val) in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({col})"
        self.query_execute(query)

    def remove_table(self, table_name: str) -> None:
        """テーブルを消す

        Parameters
        ----------
        table_name: str
            テーブル名
        """
        self.query_execute(f"DROP TABLE {table_name}")

    def insert(self, table_name: str, data: dict) -> None:
        """データをreplaceで挿入

        Parameters
        ----------
        table_name: str
            テーブル名
        data: dict
            挿入するデータ
        """
        col = ", ".join(data.keys())
        sac = ", ".join(["?"] * len(data))
        query1 = f"REPLACE INTO {table_name}({col}) values({sac})"
        self.query_execute(query1, values=tuple(data.values()))

    def delete(self, table_name: str, data: str, value: str) -> None:
        """データを消す

        Parameters
        ----------
        data: str
            キー
        data: str
            消すデータ
        """
        query = f"DELETE FROM {table_name} WHERE {data} = ?"
        self.query_execute(query, values=(value,))

    def select(
        self,
        table_name: str,
        columns: list,
        terms: str = None
    ) -> pd.DataFrame:
        """データを取得

        Parameters
        ----------
        table_name: str
            テーブル名
        columns: list
            取得対象
        terms: str = None
            条件

        Returns
        ----------
        pd.DataFrame
            取得結果
        """
        col = ", ".join(columns)
        if terms is None:
            query = f"SELECT {col} FROM {table_name}"
        else:
            query = f"SELECT {col} FROM {table_name} WHERE {terms}"

        ret = pd.read_sql(query, self.__connect)

        return ret

    def close_connect(self) -> None:
        """dbを切断する
        """
        if self.__connect is not None:
            self.__connect.close()
