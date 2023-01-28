# third party
from slack_sdk import WebClient
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

    def get_members_id(self, channel_id: str) -> tuple:

        response = self.__client.conversations_members(channel=channel_id)
        if response["ok"]:
            return response["ok"], response.get("members")
        else:
            return response["ok"], response.get("error")

    def get_member_info(self, member_id: str) -> tuple:

        response = self.__client.users_info(user=member_id)
        if response["ok"]:
            return response["ok"], response.get("user")
        else:
            return response["ok"], response.get("error")

    def get_conversations_history(
            self,
            channel_id: str
    ) -> tuple:

        response = self.__client.conversations_history(
            channel=channel_id, limit=self.__limit
        )
        if response["ok"] is False:
            ret = (response["ok"], response.get("error"))
        else:
            ret = (response["ok"], response.get("messages"))

        return ret
