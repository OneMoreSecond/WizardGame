from game.card import SuitCard
from typing import Dict, Set, List, Optional

from game import Card, Board, Suit
from helper import value_check, print_separator
from .strategy import Strategy

__all__ = [
    'HumanStrategy'
]


class HumanStrategy(Strategy):
    def __init__(self, player: int, trump: Optional[Suit], hand: Set[Card]):
        self.player = player
        self.hand = hand.copy()

        print_separator()
        self._print_hand(trump)
        print_separator()

        while True:
            prediction_str = input('Enter your prediction: ')
            try:
                self._prediction = int(prediction_str)
            except ValueError:
                print('[Error] Not an integer')
                continue
            if self._prediction < 0:
                print('[Error] Please enter a non-negative integer')
            else:
                break

    def _print_hand(self, trump: Optional[Suit]):
        print(f'Player {self.player}')
        print()
        print(f'Trump: {trump and trump.name}')
        print()
        print('Your hand:')
        if trump is not None:
            print('(T after a suit means the suit is the trump)')
        print()
        rows: Dict[str, List[str]] = {}
        rows['Special'] = sorted(str(card) for card in self.hand if card.suit is None)
        for suit in Suit:
            suit_cards: List[SuitCard] = []
            for card in self.hand:
                if card.suit == suit:
                    assert isinstance(card, SuitCard)
                    suit_cards.append(card)
            key = suit.name
            if suit == trump:
                key += '(T)'
            rows[key] = [card.rank for card in sorted(suit_cards, key=lambda card: card.standard_rank_index)]
        for key, row in rows.items():
            print(key.ljust(15), ' '.join(row) or None)

    @property
    def prediction(self) -> int:
        return self._prediction

    def play(self, board: Board) -> Card:
        value_check(self.hand is not None, 'Hand is not set')
        value_check(self._prediction is not None, 'Prediction is not set')
        assert(self.player == board.cur_player)

        print_separator()
        board.print()
        print()
        self._print_hand(board.trump)
        print_separator()

        while True:
            card_name_str = input('Enter the card to play: ')
            try:
                play = Card.parse(card_name_str)
            except ValueError as e:
                print(f'[Error] {e.args[0]}')
                continue
            if play not in self.hand:
                print('[Error] Not in your hand')
            elif not board.can_play_suit(play.suit, self.hand):
                print(f'[Error] You should play a {board.cur_leading_suit} card')
            else:
                self.hand.remove(play)
                return play
