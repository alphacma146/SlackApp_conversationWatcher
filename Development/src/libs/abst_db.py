# Standard lib
from abc import ABC, abstractmethod


class IDBManager(ABC):

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()
