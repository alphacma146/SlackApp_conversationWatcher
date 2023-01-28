# third party
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse
# Self made
from .abst_slack import ISlackIF


class SlackIF(ISlackIF):

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "__instance"):
            cls.__instance = super(SlackIF, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:

        self.__limit = 1000
        self.__client = None

    def initialize(self, token: str):

        self.__client = WebClient(token)

    def request(self, func, kwargs: dict) -> SlackResponse:

        try:
            response = func(**kwargs)
        except BaseException:
            pass

        return response

    def check(self, response: SlackResponse, target: str) -> tuple:

        if response["ok"]:
            return response["ok"], response.get(target)
        else:
            return response["ok"], response.get("error")

    def get_members_id(self, channel_id: str) -> tuple:

        res = self.request(
            self.__client.conversations_members,
            {"channel": channel_id}
        )

        return self.check(res, "members")

    def get_member_info(self, member_id: str) -> tuple:

        res = self.request(
            self.__client.users_info,
            {"user": member_id}
        )

        return self.check(res, "user")

    def get_conversations_history(self, channel_id: str) -> tuple:

        res = self.request(
            self.__client.conversations_history,
            {"channel": channel_id, "limit": self.__limit}
        )

        return self.check(res, "messages")
