# third party
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse
# Self made
from .abst_slack import ISlackIF


class SlackIF(ISlackIF):
    """slackAPIでサーバーとやり取りする
    """
    def __new__(cls, *args, **kargs):
        """constructor

        Note
        ----------
        Singleton
        """
        if not hasattr(cls, "__instance"):
            cls.__instance = super(SlackIF, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        """constructor
        """
        self.__limit = 1000
        self.__client = None

    def initialize(self, token: str) -> None:
        """webClientを初期化

        Parameters
        ----------
        token: str
            slack token
        """
        self.__client = WebClient(token)

    def request(self, func, kwargs: dict) -> SlackResponse:
        """サーバーに投げる

        Parameters
        ----------
        func
            サーバーに投げる関数
        kwargs: dict
            引数

        Returns
        ----------
        SlackResponse
        """
        try:
            response = func(**kwargs)
        except BaseException as e:
            response = e.response

        return response

    def check(self, response: SlackResponse, target: str) -> tuple:
        """サーバーに投げる

        Parameters
        ----------
        response: SlackResponse
            サーバーからのレスポンス
        target: str
            要素名

        Returns
        ----------
        tuple
            (結果bool, 内容)
        """
        if response["ok"]:
            return response["ok"], response.get(target)
        else:
            return response["ok"], response.get("error")

    def get_members_id(self, channel_id: str) -> tuple:
        """メンバーIDを取得する

        Parameters
        ----------
        channel_id: str
            チャンネルID

        Returns
        ----------
        tuple
            (結果bool, 内容)
        """
        res = self.request(
            self.__client.conversations_members,
            {"channel": channel_id}
        )

        return self.check(res, "members")

    def get_member_info(self, member_id: str) -> tuple:
        """メンバー情報を取得する

        Parameters
        ----------
        member_id: str
            メンバーID

        Returns
        ----------
        tuple
            (結果bool, 内容)
        """

        res = self.request(
            self.__client.users_info,
            {"user": member_id}
        )

        return self.check(res, "user")

    def get_conversations_history(self, channel_id: str) -> tuple:
        """会話ログを取得する

        Parameters
        ----------
        member_id: str
            メンバーID

        Returns
        ----------
        tuple
            (結果bool, 内容)
        """
        res = self.request(
            self.__client.conversations_history,
            {"channel": channel_id, "limit": self.__limit}
        )

        return self.check(res, "messages")
