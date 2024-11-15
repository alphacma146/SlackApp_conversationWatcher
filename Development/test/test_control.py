import pytest
from unittest import mock
import os
import pandas as pd
from src.control import Control


class TestControl():

    @pytest.fixture
    def test_obj(self):
        root_path_mock = mock.MagicMock()
        self.exe_path_mock = mock.MagicMock()
        target = Control(root_path_mock, self.exe_path_mock)

        self.chn_df = pd.DataFrame(
            data={
                "channel_id": ["CHANNEL_ID1", "CHANNEL_ID2"],
                "channel_name": ["CHANNELNAME1", "CHANNELNAME2"]
            }
        )
        self.mem_df = pd.DataFrame(data={
            "user_id": [
                "U04XLXCXUXX",
                "U04X7XPXJXX",
                "U04X5XBXMXX",
            ],
            "user_name": [
                "Hayashi Senjyuro",
                "Takahashi Korekiyo",
                "Saionji Kinmochi",
            ],
            "real_name": [
                "林銑十郎",
                "高橋是清",
                "西園寺公望",
            ]
        })
        self.his_df = pd.DataFrame(
            data={
                "id": ["1", "2", "3", "4", "5"],
                "user_id": ["ID1", "ID2", "ID3", "ID4", "ID5"],
                "timestamp": [10, 20, 30, 40, 50],
                "text": ["BOOJUM"] * 5,
                "reaction": [0] * 5
            }
        )

        return target

    @pytest.mark.parametrize("isexist", [
        True,
        False
    ])
    def test_isexist_dbfile(self, test_obj, isexist):
        path_mock = mock.MagicMock()
        path_mock.exists.return_value = isexist
        with mock.patch.object(
            self.exe_path_mock,
            "__truediv__",
            return_value=path_mock
        ):
            assert test_obj.isexist_dbfile() is isexist

    @pytest.mark.parametrize("isexist", [
        True,
        False
    ])
    def test_dbfile_size(self, test_obj, isexist):
        with (
            mock.patch.object(
                test_obj,
                "isexist_dbfile",
                return_value=isexist
            ),
            mock.patch.object(
                os.path,
                "getsize",
                return_value=0
            )
        ):
            assert isinstance(test_obj.dbfile_size(), float)

    @pytest.mark.parametrize("result, ret, decrypted_token, args", [
        (True, True, "", ["TOKEN", "KEY"]),
        (False, False, "db_token", [None, None]),
        (True, True, "db_token", [None, None]),
        (True, True, "new_token", [None, None]),
    ])
    def test_start_up(self, test_obj, result, ret, decrypted_token, args):
        model_mock = mock.MagicMock()
        model_mock.get_token.return_value = "db_token", "key"
        decipher_mock = mock.MagicMock()
        decipher_mock.execute.return_value = ret, decrypted_token
        with (
            mock.patch.object(test_obj, "_Control__slcIF"),
            mock.patch.object(test_obj, "_Control__model", model_mock),
            mock.patch.object(test_obj, "_Control__decipher", decipher_mock)
        ):
            assert test_obj.start_up(*args) is result

    def test_close_window(self, test_obj):
        with mock.patch.object(test_obj, "_Control__model"):
            assert test_obj.close_window() is None

    @pytest.mark.parametrize("result, ret, decrypted_token", [
        (False, False, None),
        (True, True, "db_token"),
        (True, True, "new_token"),
    ])
    def test_release_lock(self, test_obj, result, ret, decrypted_token):
        decipher_mock = mock.MagicMock()
        decipher_mock.execute.return_value = ret, decrypted_token
        with (
            mock.patch.object(test_obj, "_Control__slcIF"),
            mock.patch.object(test_obj, "_Control__model"),
            mock.patch.object(test_obj, "_Control__decipher", decipher_mock)
        ):
            assert test_obj.release_lock("key") is result

    def test_db_info(self, test_obj):
        model_mock = mock.MagicMock()
        model_mock.get_dbtable.return_value = [
            "token_meta",
            "channel_master",
            "IDDATATABLE1", "IDDATATABLE1_user_master",
            "IDDATATABLE2", "IDDATATABLE2_user_master"
        ]
        model_mock.get_member.return_value = self.mem_df
        model_mock.get_history.return_value = self.his_df
        with mock.patch.object(test_obj, "_Control__model", model_mock):
            assert isinstance(test_obj.db_info(), dict)

    @pytest.mark.parametrize("squeeze", [
        True,
        False
    ])
    def test_get_channelname_list(self, test_obj, squeeze):
        model_mock = mock.MagicMock()
        model_mock.get_channel.return_value = self.chn_df
        with mock.patch.object(test_obj, "_Control__model", model_mock):
            if squeeze:
                assert isinstance(
                    test_obj.get_channelname_list(squeeze), pd.Series
                )
            else:
                assert isinstance(
                    test_obj.get_channelname_list(squeeze), pd.DataFrame
                )

    def test_set_channel(self, test_obj):
        with mock.patch.object(test_obj, "_Control__model"):
            assert test_obj.set_channel("CHNID", "NAME") is None

    def test_del_channel(self, test_obj):
        with mock.patch.object(test_obj, "_Control__model"):
            assert test_obj.del_channel("CHNID") is None

    def test_fetch_data(self, test_obj):
        mem_data = self.mem_df
        his_data = self.his_df
        progressbar_mock = mock.MagicMock()
        progress_label_mock = mock.MagicMock()
        fetch_mock = mock.MagicMock()
        fetch_mock.execute.return_value = (True, mem_data), (True, his_data)
        with (
            mock.patch.object(test_obj, "_Control__model"),
            mock.patch.object(test_obj, "_Control__fetch", fetch_mock),
            mock.patch.object(
                test_obj,
                "convert_channel_name_id",
                return_value="CHNID"
            )
        ):
            assert test_obj.fetch_data(
                "CHNID",
                progressbar_mock,
                progress_label_mock
            ) is None

    @pytest.mark.parametrize("res1, res2, ret1, ret2, result", [
        (False, False, "ServerError", "ServerError", "ServerError"),
        (True, False, "MemberError", "ConversationError", "ConversationError"),
        (False, True, "MemberError", "ConversationError", "MemberError"),
    ])
    def test_fetch_data_anomaly(
            self,
            test_obj,
            res1,
            res2,
            ret1,
            ret2,
            result
    ):
        progressbar_mock = mock.MagicMock()
        progress_label_mock = mock.MagicMock()
        fetch_mock = mock.MagicMock()
        fetch_mock.execute.return_value = (res1, ret1), (res2, ret2)
        with (
            mock.patch.object(test_obj, "_Control__model"),
            mock.patch.object(test_obj, "_Control__fetch", fetch_mock),
            mock.patch.object(
                test_obj,
                "convert_channel_name_id",
                return_value="CHNID"
            )
        ):
            assert test_obj.fetch_data(
                "CHNID",
                progressbar_mock,
                progress_label_mock
            ) == result

    @pytest.mark.parametrize("ret1, ret2, result", [
        ("ServerError", "ResponseError", {"ResponseError", "ServerError"}),
    ])
    def test_fetch_data_anomaly2(
            self,
            test_obj,
            ret1,
            ret2,
            result
    ):
        progressbar_mock = mock.MagicMock()
        progress_label_mock = mock.MagicMock()
        fetch_mock = mock.MagicMock()
        fetch_mock.execute.return_value = (False, ret1), (False, ret2)
        with (
            mock.patch.object(test_obj, "_Control__model"),
            mock.patch.object(test_obj, "_Control__fetch", fetch_mock),
            mock.patch.object(
                test_obj,
                "convert_channel_name_id",
                return_value="CHNID"
            )
        ):
            res = test_obj.fetch_data(
                "CHNID",
                progressbar_mock,
                progress_label_mock
            )
            assert set(res.split("\n")) == result

    @pytest.mark.parametrize("ret, start, end", [
        (False, "2021/01/01", "2022/01/01"),
        (True, "2021-01-01", "2022-01-01"),
        (True, "2021/01-01", "2022-01/01"),
        (True, "ひづけ", ""),
        (True, 1564988, 159263.0231),
    ])
    def test_output_data(self, test_obj, ret, start, end):
        output_mock = mock.MagicMock()
        output_mock.execute.return_value = ret
        with (
            mock.patch.object(test_obj, "_Control__output", output_mock),
            mock.patch.object(
                test_obj,
                "convert_channel_name_id",
                return_value="CHNID"
            )
        ):
            assert test_obj.output_data(
                "output_path",
                "NAME",
                start,
                end
            ) is ret

    @pytest.mark.parametrize("target, result", [
        ("CHANNEL_ID1", "CHANNELNAME1"),
        ("CHANNELNAME2", "CHANNEL_ID2"),
        ("CHANNEL_ID9", None),
        ("CHANNELNAME9", None),
        ("BOOJUM", None),
        ("", None),
    ])
    def test_convert_channel_name_id(self, test_obj, target, result):
        with mock.patch.object(
            test_obj,
            "get_channelname_list",
            return_value=self.chn_df
        ):
            assert test_obj.convert_channel_name_id(target) == result
