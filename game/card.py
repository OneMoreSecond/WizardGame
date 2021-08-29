import enum
import itertools
from typing import Optional, Dict
from abc import ABC, abstractmethod

from helper import value_check


__all__ = [
    "Suit",
    "Card",
    "SuitCard",
    "all_suit_cards",
    "SpecialCard",
    "WizardCard",
    "JesterCard",
]


class Suit(enum.Enum):
    Spade = enum.auto()
    Heart = enum.auto()
    Diamond = enum.auto()
    Club = enum.auto()

    # pylint: disable=invalid-str-returned
    def __str__(self) -> str:
        return self.name


class Card(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @property
    def suit(self) -> Optional[Suit]:
        return None

    def __eq__(self, other: 'Card') -> bool:
        return repr(self) == repr(other)

    def __hash__(self) -> int:
        return hash(repr(self))

    @classmethod
    def _card_type(cls) -> str:
        return cls.__name__[:-len('Card')]

    @classmethod
    def parse(cls, name: str) -> 'Card':
        for subclass in cls.__subclasses__():
            try:
                return subclass.parse(name)
            except ValueError:
                pass
        raise ValueError(f'invalid card name {name}')


standard_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class SuitCard(Card):
    def __init__(self, suit: Suit, rank: str):
        self._suit = suit
        self.rank = rank
        self.standard_rank_index = standard_ranks.index(self.rank)

    @property
    def suit(self) -> Suit:
        return self._suit

    def __repr__(self) -> str:
        return f'{self.suit} {self.rank}'

    _parse_mapping: Dict[str, Card] = {}

    @classmethod
    def register_parse_mapping(cls, name: str, card: Card):
        value_check(name not in cls._parse_mapping, f'Name {name} has been registered')
        cls._parse_mapping[name] = card

    @classmethod
    def parse(cls, name: str) -> Card:
        value_check(name in cls._parse_mapping, f'Invalid card name {name}')
        return cls._parse_mapping[name]


all_suit_cards = []
for suit in Suit:
    suit_prefixes = list(map(''.join, itertools.product([suit.name, suit.name.lower()], ['', ' '])))
    for rank in standard_ranks:
        card = SuitCard(suit, rank)
        all_suit_cards.append(card)
        for suit_prefix in suit_prefixes:
            SuitCard.register_parse_mapping(suit_prefix + rank, card)


class SpecialCard(Card, ABC):
    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self) -> str:
        return f'{self._card_type()}{self.idx}'

    @classmethod
    def parse(cls, name: str) -> Card:
        try:
            card_type = cls._card_type().lower()
            value_check(name.lower().startswith(card_type), f'Invalid card name {name}')
            idx = int(name[len(card_type):])
            return cls(idx)
        except ValueError:
            for subclass in cls.__subclasses__():
                try:
                    return subclass.parse(name)
                except ValueError:
                    pass
            raise ValueError(f'invalid card name {name}')


class WizardCard(SpecialCard):
    pass


class JesterCard(SpecialCard):
    pass
