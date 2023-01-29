# Standard lib
import os
from pathlib import Path
import time
# Third party
from Crypto.Cipher import AES
# Saif made
from model import Model
from libs.slack_IF import SlackIF
from component.fetch import Fetch_Data
from component.output import Output_Data
from appconfig import get_logger, MessageText

KEY_TAIL = "TK"


class Control():

    def __init__(self, exe_path: Path, root_path: Path) -> None:

        self.__model = Model(exe_path)
        self.__slcIF = SlackIF()
        self.__fetch = Fetch_Data(self.__slcIF)
        self.__output = Output_Data(self.__model)
        self.__exe_path = exe_path
        self.__root_path = root_path

        self.__logger = get_logger(__name__)

    def isexist_dbfile(self):

        path = self.__exe_path / self.__model.get_dbfilename()

        return path.exists()

    def dbfile_size(self) -> float:

        if self.isexist_dbfile():
            ret = os.path.getsize(
                self.__exe_path / self.__model.get_dbfilename()
            )
        else:
            ret = 0

        return ret / 1024 / 1024

    def start_up(self, token: str = None):

        self.__model.initialize(first=True)
        if token is None:
            token = self.__model.get_token()
        else:
            self.__model.insert_token(token)
        self.__slcIF.initialize(token)
        self.__logger.info(token)

    def release_lock(self, key: str):

        key = (key * 2 + KEY_TAIL).encode()
        if len(key) != AES.block_size:
            return False

        with open(self.__root_path / "cripto_token.dat", "rb") as f:
            nonce, tag, ciphertext = [f.read(x) for x in (
                AES.block_size, AES.block_size, -1
            )]

        cipher = AES.new(key, AES.MODE_EAX, nonce)
        try:
            decrypted_token = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            return False

        self.start_up(decrypted_token.decode())

        return True

    def db_info(self) -> dict:

        table = self.__model.get_dbtable()
        tb_dict = {}
        for tb in table:
            user_tb = [it for it in table if it in tb]
            if len(user_tb) == 1:
                tb_dict[tb] = user_tb

        for tb in tb_dict.keys():
            mem_num = len(self.__model.get_member(tb))
            data_num = len(self.__model.get_history(tb))
            tb_dict[tb] = (mem_num, data_num)

        return tb_dict

    def get_channelname_list(self, squeeze: bool = False):

        ret = self.__model.get_channel()
        if squeeze:
            df = ret["channel_name"]
        else:
            df = ret

        return df

    def set_channel(self, chn_id: str, name: str):

        self.__model.insert_channel(chn_id, name)

    def del_channel(self, chn_id: str):

        self.__model.delete_channel(chn_id)

    def fetch_data(self, chn_name: str, progressbar, progress_label):

        chn_id = self.convert_channel_name_id(chn_name)
        self.__logger.info(chn_id)
        self.__model.create_datatable(chn_id)

        (res1, mem_data), (res2, his_data) = self.__fetch.execute(chn_id)
        total = len(his_data)
        progress_label.text = f"0 / {total}"

        match (res1, res2):
            case (False, False):
                self.__logger.info("Request Fail")
                return "\n".join({mem_data, his_data})
            case (False, True):
                self.__logger.info(f"member_info {res1}")
                return mem_data
            case (True, False):
                self.__logger.info(f"conversations_history {res2}")
                return his_data

        for data in mem_data:
            self.__model.insert_member(chn_id, data)

        for i, data in enumerate(his_data, start=1):
            self.__model.insert_history(chn_id, data)
            progress_label.text = f"{i} / {total}"
            progressbar.value = i / total * 100

    def output_data(
            self,
            save_path: str,
            chn_name: str,
            start: str = None,
            end: str = None
    ):

        def convert_timestamp(date: str) -> int:

            try:
                time_ = time.strptime(date, "%Y/%m/%d")
                ret = int(time.mktime(time_))
            except BaseException:
                ret = None

            return ret

        chn_id = self.convert_channel_name_id(chn_name)
        start = convert_timestamp(start) if start != "" else None
        end = convert_timestamp(end) if end != "" else None
        self.__output.execute(save_path, chn_id, chn_name, start, end)

    def convert_channel_name_id(self, target: str) -> str:

        chn_df = self.get_channelname_list()
        if target in (sr := chn_df["channel_name"]).to_list():
            chn_id = chn_df[sr == target]["channel_id"]
        elif target in (sr := chn_df["channel_id"]).to_list():
            chn_id = chn_df[sr == target]["channel_name"]
        else:
            return None

        chn_id = chn_id.to_string(index=False)

        return chn_id
