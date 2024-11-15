import pytest
from unittest import mock
from src.component.fetch import FetchData


class TestFetchData():

    @pytest.fixture
    def test_obj(self):
        self.slcIF_mock = mock.MagicMock()
        target = FetchData(self.slcIF_mock)

        return target

    def test_execute(self, test_obj):
        with (
            mock.patch.object(
                test_obj,
                "_FetchData__get_member",
                return_value={}
            ),
            mock.patch.object(
                test_obj,
                "_FetchData__get_history",
                return_value={}
            )
        ):
            assert test_obj.execute("chn_id")

    @pytest.mark.parametrize("mem_res, mem_data, mem_info", [
        (False, "ServerError", None),
        (
            True,
            [
                "U04XZXRXJX4",
                "U04XLXCXUXK",
            ],
            [
                True,
                {}
            ]
        ),
        (
            True,
            [
                "U04XZXRXJX4",
                "U04XLXCXUXK",
            ],
            [
                False,
                {}
            ]
        )
    ])
    def test___get_member(self, test_obj, mem_res, mem_data, mem_info):
        with (
            mock.patch.object(
                self.slcIF_mock,
                "get_members_id",
                return_value=(mem_res, mem_data)
            ),
            mock.patch.object(
                self.slcIF_mock,
                "get_member_info",
                return_value=mem_info
            )
        ):
            assert test_obj._FetchData__get_member("chn_id")

    @pytest.mark.parametrize("his_res, his_data", [
        (False, "ServerError"),
        (
            True,
            [
                {
                    "client_msg_id": "xxxxx",
                    "text": "テキスト",
                    "user": "U0XXXXXXXXX",
                    "ts": "1600000000.000000",
                    "reactions": [
                        {
                            "name": "stamp",
                            "users": ["UXXXXXXX"],
                            "count": 1
                        },
                        {
                            "name": "stamp",
                            "users": ["UYYYYYY"],
                            "count": 1
                        }
                    ]
                },
                {
                    "client_msg_id": "xxxxx",
                    "text": "テキスト",
                    "user": "U0XXXXXXXXX",
                    "ts": "1600000000.000000",
                },
                {
                    "type": "message",
                    "subtype": "group_join",
                    "ts": "1600000000.000000",
                    "user": "U0XXXXXXXXX",
                    "text": "<BOOJUM>さんがグループに参加しました"
                }
            ]
        ),
    ])
    def test___get_history(self, test_obj, his_res, his_data):
        with mock.patch.object(
            self.slcIF_mock,
            "get_conversations_history",
            return_value=(his_res, his_data)
        ):
            assert test_obj._FetchData__get_history("chn_id")
