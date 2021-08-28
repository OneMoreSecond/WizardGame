import enum
from typing import Optional
from abc import ABC, abstractmethod, abstractproperty

__all__ = [
    "Suit",
    "standard_ranks",
    "Card",
    "SuitCard",
    "WizardCard",
    "JesterCard",
    "all_suit_cards",
]


class Suit(enum.Enum):
    Spade = enum.auto()
    Heart = enum.auto()
    Diamond = enum.auto()
    Club = enum.auto()


standard_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'K', 'A']


class Card(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractproperty
    def suit(self) -> Optional[Suit]:
        return None


class SuitCard(Card):
    suit: Suit
    rank: str

    def __init__(self, suit: Suit, rank: str):
        self.suit = suit
        self.rank = rank
        self.standard_rank_index = standard_ranks.index(self.rank)

    @property
    def __str__(self) -> str:
        return f'{self.suit.name} {self.rank}'


class WizardCard(Card):
    def __str__(self) -> str:
        return 'Wizard'


class JesterCard(Card):
    def __str__(self) -> str:
        return 'Jester'


all_suit_cards = []
for suit in Suit:
    for rank in standard_ranks:
        all_suit_cards.append(SuitCard(suit, rank))
