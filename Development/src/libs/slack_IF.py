# third party
from slack_sdk import WebClient
# Self made
from abst_slack import ISlackIF


class SlackIF(ISlackIF):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "__instance"):
            cls.__instance = super(SlackIF, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.__limit = 1000

    def get_client(self, token: str) -> WebClient:

        return WebClient(token)

    def get_members_info(self, client: WebClient, channel_id: str) -> tuple:

        response = client.conversations_members(channel=channel_id)
        if response["ok"] is False:
            return response["ok"], response.get("error")

        user_ids = response["members"]
        ret = {
            user_data["id"]: user_data["real_name"]
            for user_data
            in [client.users_info(user=user).get("user") for user in user_ids]
        }

        return response["ok"], ret

    def get_conversations_history(
            self,
            client: WebClient,
            channel_id: str
    ) -> tuple:

        response = client.conversations_history(
            channel=channel_id, limit=self.__limit
        )
        if response["ok"] is False:
            ret = (response["ok"], response.get("error"))
        else:
            ret = (response["ok"], response.get("messages"))

        return ret
