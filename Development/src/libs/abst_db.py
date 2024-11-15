# Standard lib
from abc import ABC, abstractmethod


class IDBManager(ABC):
    """DBManager抽象クラス

    Attributes
    ----------
    """
    @abstractmethod
    def initialize(self):
        """初期化
        """
        raise NotImplementedError()

    @abstractmethod
    def query_execute(self):
        """クエリ発行
        """
        raise NotImplementedError()

    @abstractmethod
    def get_table_all(self):
        """テーブル一覧取得
        """
        raise NotImplementedError()

    @abstractmethod
    def create_table(self):
        """テーブル作成
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_table(self):
        """テーブル削除
        """
        raise NotImplementedError()

    @abstractmethod
    def insert(self):
        """データ挿入
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self):
        """データ削除
        """
        raise NotImplementedError()

    @abstractmethod
    def select(self):
        """データ取得
        """
        raise NotImplementedError()

    @abstractmethod
    def close_connect(self):
        """切断
        """
        raise NotImplementedError()
