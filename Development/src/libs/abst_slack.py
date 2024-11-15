# Standard lib
from abc import ABC, abstractmethod


class ISlackIF(ABC):
    """SlackIF抽象クラス

    Attributes
    ----------
    """
    @abstractmethod
    def initialize(self):
        """初期化
        """
        raise NotImplementedError()

    @abstractmethod
    def request(self):
        """slackAPIからサーバーにリクエストする
        """
        raise NotImplementedError()

    @abstractmethod
    def check(self):
        """サーバーからの戻り値をチェックする
        """
        raise NotImplementedError()

    @abstractmethod
    def get_members_id(self):
        """メンバーIDを取得
        """
        raise NotImplementedError()

    @abstractmethod
    def get_member_info(self):
        """メンバー情報を取得
        """
        raise NotImplementedError()

    @abstractmethod
    def get_conversations_history(self):
        """会話ログを取得
        """
        raise NotImplementedError()
