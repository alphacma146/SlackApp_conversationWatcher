# Standard lib
from pathlib import Path
import sqlite3
from sqlite3 import Cursor


class DB_Manager():

    def __init__(self, exe_path: Path) -> None:
        self.__exe_path = exe_path
        self.__db_name = "SlackLogAccumulator.db"

    def initialize(self) -> None:
        self.__connect = sqlite3.connect(self.__exe_path / self.__db_name)

    def get_cursor(self) -> Cursor:
        return self.__connect.cursor()

    def create_table(self, cursor: Cursor):
        pass

    def get_table_all(self) -> list:
        pass

    def insert_data(self):
        pass

    def get_data(self):
        pass

    def close_connect(self) -> None:
        pass
