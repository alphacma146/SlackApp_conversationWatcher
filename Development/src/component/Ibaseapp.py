# Standard lib
from abc import ABC, abstractmethod


class IBaseApp(ABC):

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()
