import pytest
from src.component.abst_app import IAppFunction, BaseAppFunction


class TestIAppFunction():

    IAppFunction.__abstractmethods__ = set()

    @pytest.fixture
    def test_obj(self):

        return IAppFunction()

    def test_initialize(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.initialize()

    def test_execute(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.execute()


class TestBaseAppFunction():

    @pytest.fixture
    def test_obj(self):
        return BaseAppFunction()

    def test_initialize(self, test_obj):
        assert test_obj.initialize() is None

    def test_execute(self, test_obj):
        assert test_obj.execute() is None
