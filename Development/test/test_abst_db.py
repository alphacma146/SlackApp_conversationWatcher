import pytest
from src.libs.abst_db import IDBManager


class TestIAppFunction():

    IDBManager.__abstractmethods__ = set()

    @pytest.fixture
    def test_obj(self):

        return IDBManager()

    def test_initialize(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.initialize()

    def test_query_execute(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.query_execute()

    def test_get_table_all(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.get_table_all()

    def test_create_table(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.create_table()

    def test_remove_table(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.remove_table()

    def test_insert(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.insert()

    def test_delete(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.delete()

    def test_select(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.select()

    def test_close_connect(self, test_obj):
        with pytest.raises(NotImplementedError):
            test_obj.close_connect()
