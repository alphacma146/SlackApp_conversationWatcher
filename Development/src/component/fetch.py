# Standard lib
from concurrent.futures import ThreadPoolExecutor
# Third party
# Saif made
from .abst_app import BaseAppFunction


class FetchData(BaseAppFunction):
    """slackAPIでサーバーから情報を取得する
    """

    def __init__(self, slcIF):
        """constructor

        Parameters
        ----------
        slcIF
        """
        super().__init__()
        self.__slcIF = slcIF

    def execute(self, chn_id: str) -> tuple:
        """実行処理

        Parameters
        ----------
        chn_id: str
            チャンネルID

        Returns
        ----------
        tuple
            (結果bool, 内容)

        Note
        ----------
        マルチスレッドでリクエストを投げる
        """
        with ThreadPoolExecutor(max_workers=4) as executor:
            future = {
                key: executor.submit(func, chn_id) for (key, func) in {
                    "mem": self.__get_member,
                    "his": self.__get_history,
                }.items()
            }

        mem_res = future["mem"].result()
        his_res = future["his"].result()

        return mem_res, his_res

    def __get_member(self, chn_id: str) -> tuple:
        """メンバー情報を取得

        Parameters
        ----------
        chn_id: str
            チャンネルID

        Returns
        ----------
        tuple
            (結果bool, 内容)
        """
        mem_res, mem_data = self.__slcIF.get_members_id(chn_id)
        if not mem_res:
            return mem_res, mem_data

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
        """会話ログを取得

        Parameters
        ----------
        chn_id: str
            チャンネルID

        Returns
        ----------
        tuple
            (結果bool, 内容)
        """
        def total_reaction(reactions: list) -> int:

            if reactions is None:
                ret = 0
            else:
                ret = sum([item.get("count") for item in reactions])

            return ret

        his_res, his_data = self.__slcIF.get_conversations_history(chn_id)
        if not his_res:
            return his_res, his_data

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
