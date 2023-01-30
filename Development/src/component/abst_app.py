# Standard lib
from abc import ABC, abstractmethod


class IAppFunction(ABC):
    """機能抽象クラス

    Attributes
    ----------
    """

    @abstractmethod
    def initialize(self) -> None:
        """初期化
        """
        raise NotImplementedError()

    @abstractmethod
    def execute(self) -> None:
        """機能実行
        """
        raise NotImplementedError()


class BaseAppFunction(IAppFunction):
    """機能基底クラス

    Attributes
    ----------
    """

    def initialize(self) -> None:
        """初期化
        """
        pass
