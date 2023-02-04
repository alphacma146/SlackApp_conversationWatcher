# Standard lib
import os
from pathlib import Path
import time
# Third party
from Crypto.Cipher import AES
import pandas as pd
# Saif made
from model import Model
from libs.slack_if import SlackIF
from component.fetch import FetchData
from component.output import OutputData
from component.decipher import Decipher
from appconfig import get_logger

KEY_TAIL = "TK"


class Control():
    """動作を定義
    """

    def __init__(self, root_path: Path, exe_path: Path):
        """constructor

        Parameters
        ----------
        root_path: Path
            実行ファイルパス
        exe_path: Path
            exeファイルパス
        """
        self.__exe_path = exe_path
        self.__root_path = root_path
        self.__model = Model(exe_path)
        self.__slcIF = SlackIF()
        self.__fetch = FetchData(self.__slcIF)
        self.__output = OutputData(self.__model)
        self.__decipher = Decipher(self.__root_path / "cripto_token.dat")

        self.__logger = get_logger(__name__)

    def isexist_dbfile(self) -> bool:
        """dbファイルの存在チェック

        Returns
        ----------
        bool
            dbファイルがあったらTrue
        """
        path = self.__exe_path / self.__model.get_dbfilename()

        return path.exists()

    def dbfile_size(self) -> float:
        """dbファイルサイズを返す

        Returns
        ----------
        float
            dbファイルがなければ0
        """
        if self.isexist_dbfile():
            ret = os.path.getsize(
                self.__exe_path / self.__model.get_dbfilename()
            )
        else:
            ret = 0

        return ret / 1024 / 1024

    def start_up(self, token: str = None, key: str = None) -> None:
        """起動時の処理

        Parameters
        ----------
        token: str = None
            slack token文字列
        key: str = None
            解読キー文字列
        """
        match (token, key):
            # 通常起動
            case (None, None):
                self.__model.initialize()
                db_token, key = self.__model.get_token()
                ret, decrypted_token = self.__decipher.execute(key)
                # cryptoキーが変わった
                if not ret:
                    return False
                # ファイルの中身が違う
                elif db_token != decrypted_token:
                    self.__model.insert_token(decrypted_token, key)
                    token = decrypted_token
                # 起動成功
                else:
                    token = db_token
            # 初回起動
            case (_, _):
                self.__model.initialize(first=True)
                self.__model.insert_token(token, key)

        self.__slcIF.initialize(token)
        self.__logger.info(token)

        return True

    def close_window(self) -> None:
        """終了時の処理
        """
        self.__model.finalize()

    def release_lock(self, key: str) -> bool:
        """暗号化解除を試みる

        Parameters
        ----------
        key: str
            ユーザー入力の解除キー文字列

        Returns
        ----------
        bool
            解除成功だとTrue
        """
        ret, decrypted_token = self.__decipher.execute(key)

        if not ret:
            return False

        self.start_up(decrypted_token, key)

        return True

    def db_info(self) -> dict:
        """db情報を取得

        Returns
        ----------
        dict
            {"data table name":(人数, レコード数)}
        """
        table = self.__model.get_dbtable()
        tb_dict = {}
        for tb in table:
            user_tb = [it for it in table if it in tb]
            if len(user_tb) != 1:
                continue
            mem_num = len(self.__model.get_member(tb))
            data_num = len(self.__model.get_history(tb))
            tb_dict[tb] = (mem_num, data_num)

        return tb_dict

    def get_channelname_list(self, squeeze: bool = False) -> pd.DataFrame:
        """チャンネル一覧を取得する

        Parameters
        ----------
        squeeze: bool = False
            Trueでchannel_nameのSeriesを返す

        Returns
        ----------
        pd.DataFrame or pd.Series
        """
        ret = self.__model.get_channel()
        if squeeze:
            df = ret["channel_name"]
        else:
            df = ret

        return df

    def set_channel(self, chn_id: str, name: str) -> None:
        """チャンネルをdbに登録する

        Parameters
        ----------
        chn_id: str
            チャンネルID
        name: str
            チャンネル名
        """
        self.__model.insert_channel(chn_id, name)

    def del_channel(self, chn_id: str) -> None:
        """チャンネルをdbから削除

        Parameters
        ----------
        chn_id: str
            チャンネルID
        """
        self.__model.delete_channel(chn_id)

    def fetch_data(
            self,
            chn_name: str,
            progressbar,
            progress_label
    ) -> pd.DataFrame:
        """ログデータを取得

        Parameters
        ----------
        chn_name: str
            チャンネル名
        progressbar
            プログレスバーオブジェクト
        progress_label
            プログレスラベルオブジェクト

        Returns
        ----------
        pd.DataFrame

        Note
        ----------
        取得エラーだとエラーメッセージを返す
        """
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
    ) -> None:
        """ログデータを出力

        Parameters
        ----------
        save_path: str
            csvを出力するパス
        chn_name: str
            対象のチャンネル名
        start: str = None
            日付の指定
        end: str = None
            日付の指定

        Note
        ----------
        日付に変換できない文字列だと指定なしで出力
        """
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
        ret = self.__output.execute(save_path, chn_id, chn_name, start, end)

        return ret

    def convert_channel_name_id(self, target: str) -> str:
        """チャンネルIDと名前を相互変換する

        Parameters
        ----------
        target: str
            変換対象

        Returns
        ----------
        str
            変換後

        Note
        ----------
        変換できなかったらNone
        """
        chn_df = self.get_channelname_list()
        if target in (sr := chn_df["channel_name"]).to_list():
            chn_id = chn_df[sr == target]["channel_id"]
        elif target in (sr := chn_df["channel_id"]).to_list():
            chn_id = chn_df[sr == target]["channel_name"]
        else:
            return None

        chn_id = chn_id.to_string(index=False)

        return chn_id
