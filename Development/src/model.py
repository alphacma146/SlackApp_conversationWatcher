# Standard lib
from pathlib import Path
# Saif made
from libs.DB_manager import DBManager


class Model():

    def __init__(self, exe_path: Path) -> None:

        self.__db_name = "SlackLogAccumulator.db"
        self.__DBMngr = DBManager()
        self.__exe_path = exe_path

    def initialize(self):

        self.__cursor = self.__DBMngr.initialize(
            self.__exe_path / self.__db_name
        )

    def get_dbfilename(self):

        return self.__db_name

    def get_dbtable(self):

        return self.__DBMngr.get_table_all(self.__cursor)
