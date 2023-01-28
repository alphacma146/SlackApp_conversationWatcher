# Standard lib
from abc import ABC, abstractmethod


class IAppFunction(ABC):

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()


class BaseAppFunction(IAppFunction):

    def initialize(self) -> None:
        pass
