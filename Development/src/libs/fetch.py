# Standard lib
# Third party
# Saif made
from .abst_app import BaseAppFunction


class Fetch_Data(BaseAppFunction):

    def __init__(self, slcIF) -> None:
        super().__init__()
        self.__slcIF = slcIF

    def execute(self, chn_id: str) -> tuple:

        mem_res = self.__get_member(chn_id)
        his_res = self.__get_history(chn_id)

        return mem_res, his_res

    def __get_member(self, chn_id: str) -> tuple:

        mem_res, mem_data = self.__slcIF.get_members_id(chn_id)
        mem_info = [
            self.__slcIF.get_member_info(mem_id) for mem_id in mem_data
        ]
        if all([res for (res, _) in mem_info]):
            mem_data = [
                {
                    "user_id": info.get("id"),
                    "user_name": info.get("name"),
                    "real_name": info.get("real_name")
                } for (_, info) in mem_info
            ]
        else:
            mem_data = [{} for _ in range(len(mem_info))]

        return mem_res, mem_data

    def __get_history(self, chn_id: str) -> tuple:

        def total_reaction(reactions: list) -> int:

            if reactions is None:
                ret = 0
            else:
                ret = sum([item.get("count") for item in reactions])

            return ret

        his_res, his_data = self.__slcIF.get_conversations_history(chn_id)
        # メッセージ以外の投稿を除外
        his_data = [
            data for data in his_data
            if data.get("client_msg_id") is not None
        ]
        his_data = [
            {
                "id": data.get("client_msg_id"),
                "user_id": data.get("user"),
                "timestamp": data.get("ts"),
                "text": data.get("text"),
                "reaction": total_reaction(data.get("reactions")),
            } for data in his_data
        ]

        return his_res, his_data
