from typing import Set, List

from game import Card, Board
from helper import value_check
from .strategy import Strategy

__all__ = [
    'HumanStrategy'
]


def print_separator():
    print('-' * 20)


class HumanStrategy(Strategy):
    def __init__(self, player: int, hand: Set[Card]):
        self.player = player
        self.hand = hand.copy()

        print_separator()
        self._print_hand()
        print_separator()

        while True:
            prediction_str = input('Enter your prediction: ')
            try:
                self.prediction = int(prediction_str)
            except ValueError:
                print('[Error] Not an integer')
                continue
            if self.prediction < 0:
                print('[Error] Please enter a non-negative integer')
            else:
                break

    def _print_cards(self, cards: Set[Card], prompt: str = ''):
        if prompt != '':
            print(prompt)
        handlers = {}
        handlers['Special'] = {
            'cond': lambda card: card.suit is None,
            'map': str,
        }
        for suit in Suit:
            handlers[suit.name] = {
                'cond': lambda card: card.suit == suit.name,
                'map': lambda card: card.rank,
            }
        for key, handler in handlers:
            print(key, ''.join(handler['map'](card) for card in cards if handler['cond'](card)))

    def _print_hand(self):
        print(f'Player {self.player}')
        self._print_cards(self.hand, prompt='Your hand:')

    def _print_board(self, board: Board):
        print('Board:')
        print('(star after a card means the player is the round leader)')

        def print_row(cells: List[str]):
            column_width = 15
            print(''.join(cell.ljust(column_width) for cell in cells))

        print_row(['Round'] + [f'Player{player}' for player in board.players])

        for round, (leader, plays) in enumerate(zip(board.round_leaders, board.plays)):
            play_strs = list(map(str, plays))
            play_strs[leader] += '*'
            print_row([str(round)] + play_strs)

    def predict(self) -> int:
        return self.prediction

    def play(self, board: Board) -> Card:
        value_check(self.hand is not None, 'Hand is not set')
        value_check(self.prediction is not None, 'Prediction is not set')
        assert(self.player == board.cur_player)

        print_separator()
        self._print_board(board)
        print()
        self._print_hand()
        print_separator()

        while True:
            card_name_str = input('Enter the card to play: ')
            try:
                play = Card.parse(card_name_str)
            except ValueError:
                print('[Error] Not a valid card')
                continue
            if play not in self.hand:
                print('[Error] Not in your hand')
            elif not board.can_play_suit(play.suit, self.hand):
                print(f'[Error] You should play a {board.cur_leading_suit} card')
            else:
                self.hand.remove(play)
                return play
