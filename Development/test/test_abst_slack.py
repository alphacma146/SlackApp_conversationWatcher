import pytest
from src.libs.abst_slack import ISlackIF


class TestIAppFunction():

    ISlackIF.__abstractmethods__ = set()

    @pytest.fixture
    def test_obj(self):

        return ISlackIF()

    def test_initialize(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.initialize()

    def test_request(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.request()

    def test_check(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.check()

    def test_get_members_id(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.get_members_id()

    def test_get_member_info(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.get_member_info()

    def test_get_conversations_history(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.get_conversations_history()
