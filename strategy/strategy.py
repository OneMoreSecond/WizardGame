from typing import Set
from abc import ABC, abstractmethod

from game import Card, Board

__all__ = [
    'Strategy'
]


class Strategy(ABC):
    @abstractmethod
    def predict(self, hand: Set[Card]) -> int:
        raise NotImplementedError

    @abstractmethod
    def play(self, board: Board) -> Card:
        raise NotImplementedError
