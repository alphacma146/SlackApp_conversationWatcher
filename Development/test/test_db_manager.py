import pytest
from unittest import mock
import sqlite3
import pandas as pd
from src.libs.db_manager import DBManager


class TestSlackIF():

    @pytest.fixture
    def test_obj(self):
        target = DBManager()

        return target

    def test_initialize(self, test_obj):
        with mock.patch.object(sqlite3, "connect"):
            assert test_obj.initialize("db_path") is None

    def test_query_execute(self, test_obj):
        with (
            mock.patch.object(test_obj, "_DBManager__cursor"),
            mock.patch.object(test_obj, "_DBManager__connect")
        ):
            assert test_obj.query_execute("SELECT *") is None
            assert test_obj.query_execute("SELECT *", "value") is None

    def test_get_table_all(self, test_obj):
        cursor_mock = mock.MagicMock()
        cursor_mock.fetchall = mock.MagicMock(
            return_value=[
                (1, "NAME", 3, 4, 5),
                (1, "name", 3, 4, 5)
            ]
        )
        with (
            mock.patch.object(test_obj, "_DBManager__cursor", cursor_mock),
            mock.patch.object(test_obj, "_DBManager__connect")
        ):
            assert test_obj.get_table_all() == ["NAME", "name"]

    def test_create_table(self, test_obj):
        columns = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "token": "TEXT NOT NULL",
            "password": "TEXT NOT NULL",
            "date": "TEXT NOT NULL"
        }
        with (
            mock.patch.object(test_obj, "_DBManager__cursor"),
            mock.patch.object(test_obj, "_DBManager__connect")
        ):
            assert test_obj.create_table("table", columns) is None

    def test_remove_table(self, test_obj):
        with (
            mock.patch.object(test_obj, "_DBManager__cursor"),
            mock.patch.object(test_obj, "_DBManager__connect")
        ):
            assert test_obj.remove_table("table") is None

    def test_insert(self, test_obj):
        data = {
            "id": 1,
            "token": "xxxx_xxxxxxxxxx",
            "password": "PASSWORD",
            "date": "9999/99/99 99:99:99"
        }
        with (
            mock.patch.object(test_obj, "_DBManager__cursor"),
            mock.patch.object(test_obj, "_DBManager__connect")
        ):
            assert test_obj.insert("table", data) is None

    def test_delete(self, test_obj):
        primary_key = "channel_id"
        value = "D123456789",
        with (
            mock.patch.object(test_obj, "_DBManager__cursor"),
            mock.patch.object(test_obj, "_DBManager__connect")
        ):
            assert test_obj.delete("table", primary_key, value) is None

    @pytest.mark.parametrize("terns", [
        None,
        "BETWEEN A AND B",
        "timestamp >= A",
        "timestamp <= B",
    ])
    def test_select(self, test_obj, terns):
        df_mock = mock.MagicMock()
        columns = ["user_id", "user_name", "real_name"]
        with mock.patch.object(pd, "read_sql", return_value=df_mock):
            assert test_obj.select("table", columns, terns) is df_mock

    def test_close_connect(self, test_obj):
        with mock.patch.object(test_obj, "_DBManager__connect"):
            assert test_obj.close_connect() is None
