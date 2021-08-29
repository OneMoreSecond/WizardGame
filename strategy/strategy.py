from abc import ABC, abstractmethod

from game import Card, Board

__all__ = [
    'Strategy'
]


class Strategy(ABC):
    @property
    @abstractmethod
    def prediction(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def play(self, board: Board) -> Card:
        raise NotImplementedError

    @classmethod
    def strategy_type(cls) -> str:
        return cls.__name__[:-len('Strategy')]
