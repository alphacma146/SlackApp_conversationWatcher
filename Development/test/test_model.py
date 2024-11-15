import pytest
from unittest import mock
import pandas as pd
from src.model import Model


class TestModel():

    @pytest.fixture
    def test_obj(self):
        exe_path_mock = mock.MagicMock()
        target = Model(exe_path_mock)

        return target

    @pytest.mark.parametrize("first", [
        True,
        False
    ])
    def test_initialize(self, test_obj, first):
        with mock.patch.object(test_obj, "_Model__DBMngr"):
            assert test_obj.initialize(first) is None

    def test_finalize(self, test_obj):
        with mock.patch.object(test_obj, "_Model__DBMngr"):
            assert test_obj.finalize() is None

    def test_get_dbfilename(self, test_obj):
        assert isinstance(test_obj.get_dbfilename(), str)

    def test_get_dbtable(self, test_obj):
        DBMngr_mock = mock.MagicMock()
        DBMngr_mock.get_table_all.return_value = [
            "sqlite_sequence",
            "token_meta",
            "channel_master",
            "IDDATATABLE1", "IDDATATABLE1_user_master",
            "IDDATATABLE2", "IDDATATABLE2_user_master"
        ]
        result = [
            "IDDATATABLE1", "IDDATATABLE1_user_master",
            "IDDATATABLE2", "IDDATATABLE2_user_master"
        ]
        with mock.patch.object(test_obj, "_Model__DBMngr", DBMngr_mock):
            assert test_obj.get_dbtable() == result

    def test_insert_token(self, test_obj):
        with mock.patch.object(test_obj, "_Model__DBMngr"):
            assert test_obj.insert_token("TOKEN", "PASS") is None

    def test_get_token(self, test_obj):
        DBMngr_mock = mock.MagicMock()
        DBMngr_mock.select.return_value = pd.DataFrame(
            data={
                "id": [1, 2, 3],
                "token": ["token1", "token2", "token3"],
                "password": ["pass1", "pass2", "pass3"],
                "date": [
                    "2045/12/05 18:31:30.999999",
                    "2045/12/05 18:31:29.999999",
                    "2045/12/05 18:31:28.999999"
                ]
            }
        )
        with mock.patch.object(test_obj, "_Model__DBMngr", DBMngr_mock):
            assert test_obj.get_token() == ("token1", "pass1")

    def test_insert_channel(self, test_obj):
        with mock.patch.object(test_obj, "_Model__DBMngr"):
            assert test_obj.insert_channel("CHNID", "NAME") is None

    def test_delete_channel(self, test_obj):
        with mock.patch.object(test_obj, "_Model__DBMngr"):
            assert test_obj.delete_channel("CHNID") is None

    def test_get_channel(self, test_obj):
        df_mock = mock.MagicMock()
        DBMngr_mock = mock.MagicMock()
        DBMngr_mock.select.return_value = df_mock
        with mock.patch.object(test_obj, "_Model__DBMngr", DBMngr_mock):
            assert test_obj.get_channel() is df_mock

    def test_create_datatable(self, test_obj):
        with mock.patch.object(test_obj, "_Model__DBMngr"):
            assert test_obj.create_datatable("CHNID") is None

    def test_insert_member(self, test_obj):
        with mock.patch.object(test_obj, "_Model__DBMngr"):
            assert test_obj.insert_member(
                "CHNID", {
                    "user_id": "USERID",
                    "user_name": "NAME",
                    "real_name": "名前"
                }
            ) is None

    def test_get_member(self, test_obj):
        df_mock = mock.MagicMock()
        DBMngr_mock = mock.MagicMock()
        DBMngr_mock.select.return_value = df_mock
        with mock.patch.object(test_obj, "_Model__DBMngr", DBMngr_mock):
            assert test_obj.get_member("CHNID") is df_mock

    def test_insert_history(self, test_obj):
        with mock.patch.object(test_obj, "_Model__DBMngr"):
            assert test_obj.insert_history(
                "CHNID", {
                    "id": "CONVERSATIONID",
                    "user_id": "USERID",
                    "timestamp": 16000000.000000,
                    "text": "BOOJUM",
                    "reaction": 10
                }
            ) is None

    @pytest.mark.parametrize("start, end", [
        (None, None),
        (1600000000, None),
        (None, 1600000000),
        (1600000000, 1600000000)
    ])
    def test_get_history(self, test_obj, start, end):
        df_mock = mock.MagicMock()
        DBMngr_mock = mock.MagicMock()
        DBMngr_mock.select.return_value = df_mock
        with mock.patch.object(test_obj, "_Model__DBMngr", DBMngr_mock):
            assert test_obj.get_history("CHNID", start, end) is df_mock
