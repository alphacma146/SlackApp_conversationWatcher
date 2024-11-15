import pytest
from unittest import mock
import slack_sdk
from src.libs.slack_if import SlackIF


class TestSlackIF():

    @pytest.fixture
    def test_obj(self):
        target = SlackIF()

        return target

    def test_initialize(self, test_obj):
        with mock.patch.object(slack_sdk, "WebClient"):
            assert test_obj.initialize("token_string") is None

    def test_request(self, test_obj):
        res_mock = mock.MagicMock()
        func_mock = mock.MagicMock(return_value=res_mock)
        assert test_obj.request(func_mock, {"arg1": "arg1"}) is res_mock

    @pytest.mark.parametrize("target, response", [
        ("messages", {"ok": True, "messages": {}}),
        ("members", {"ok": True, "members": {}}),
        ("user", {"ok": True, "user": {}}),
        ("messages", {"ok": False, "error": "ServerError"}),
        ("members", {"ok": False, "error": "ServerError"}),
        ("user", {"ok": False, "error": "ServerError"}),
    ])
    def test_check(self, test_obj, target, response):
        res = (response["ok"], list(response.values())[-1])
        assert test_obj.check(response, target) == res

    def test_get_members_id(self, test_obj):
        client_mock = mock.MagicMock()
        client_mock.conversations_members = mock.MagicMock(
            return_value={"ok": True, "members": {}}
        )
        with mock.patch.object(test_obj, "_SlackIF__client", client_mock):
            assert test_obj.get_members_id("channel_id") == (True, {})

    def test_get_member_info(self, test_obj):
        client_mock = mock.MagicMock()
        client_mock.users_info = mock.MagicMock(
            return_value={"ok": True, "user": {}}
        )
        with mock.patch.object(test_obj, "_SlackIF__client", client_mock):
            assert test_obj.get_member_info("channel_id") == (True, {})

    def test_get_conversations_history(self, test_obj):
        client_mock = mock.MagicMock()
        client_mock.conversations_history = mock.MagicMock(
            return_value={"ok": True, "messages": {}}
        )
        with mock.patch.object(test_obj, "_SlackIF__client", client_mock):
            assert test_obj.get_conversations_history(
                "channel_id"
            ) == (True, {})
