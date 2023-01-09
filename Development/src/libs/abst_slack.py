# Standard lib
from abc import ABC, abstractmethod


class ISlackIF(ABC):

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()


class BaseSlackIF(ISlackIF):
    pass
