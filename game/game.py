import random
import typing
from typing import List, Set, Optional, Iterable

from helper import value_check
from .card import Suit, Card, SuitCard, WizardCard, JesterCard, all_suit_cards

__all__ = [
    'Board',
    'StandardGame',
]


class Board:
    """ All public information in the game (readonly for players) """

    def __init__(self, game: 'StandardGame'):
        self._game = game
        self.predictions: Optional[List[int]] = None
        self.round_leaders = []
        self.plays: List[List[Optional[Card]]] = []
        self._next_round(leader=random.randint(0, self.n_player - 1))

    def _next_round(self, leader: int):
        assert leader < self.n_player
        self.round_leaders.append(leader)
        self.plays.append([None] * self.n_player)

    @property
    def n_player(self) -> int:
        return self._game.n_player

    @property
    def players(self) -> Iterable[int]:
        return self._game.players

    @property
    def n_round(self) -> int:
        return self._game.n_round

    @property
    def trump(self) -> Optional[Suit]:
        return self._game.trump

    @property
    def round_winners(self) -> List[int]:
        return self.round_leaders[1:]

    @property
    def n_finished_round(self) -> int:
        return len(self.round_winners)

    @property
    def cur_round(self) -> int:
        return self.n_finished_round

    @property
    def cur_leader(self) -> int:
        return self.round_leaders[-1]

    @property
    def cur_round_plays(self) -> List[Optional[Card]]:
        return self.plays[-1]

    @property
    def cur_round_play_order(self) -> List[int]:
        return [(self.cur_leader + i) % self.n_player for i in range(self.n_player)]

    @property
    def cur_player(self) -> Optional[int]:
        for i in self.cur_round_play_order:
            if self.cur_round_plays[i] is None:
                return i
        return None

    @property
    def cur_leading_suit(self) -> Optional[Suit]:
        for i in self.cur_round_play_order:
            play = self.cur_round_plays[i]
            if play is None:
                return None
            elif play.suit is not None:
                return play.suit
        return None

    def can_play_suit(self, suit: Optional[Suit], hand: Set[Card]) -> bool:
        if suit is None:
            return True
        leading_suit = self.cur_leading_suit
        if leading_suit is None or all(card.suit != leading_suit for card in hand):
            return True
        return suit == leading_suit

    @property
    def is_round_play_finished(self) -> bool:
        return self.cur_player is None

    def winned_rounds(self) -> List[int]:
        return [self.round_winners.count(player) for player in range(self.n_player)]

    @property
    def is_all_finished(self) -> bool:
        return self.predictions is not None and self.n_finished_round == self._game.n_round


class StandardGame:
    def __init__(self, n_player: int = 4, n_wizard: int = 4, n_jester: int = 4, n_round: Optional[int] = None):
        value_check(n_player > 0, 'n_player should be positive')
        value_check(n_wizard > 0, 'n_wizard should be positive')
        value_check(n_jester > 0, 'n_jester should be positive')
        value_check(n_round is None or n_round > 0, 'n_round should be positive')

        self.n_player = n_player
        self.board = Board(self)

        # shuffle and make hands
        shuffled_cards = all_suit_cards.copy()
        shuffled_cards += [WizardCard(i) for i in range(n_wizard)]
        shuffled_cards += [JesterCard(i) for i in range(n_jester)]
        random.shuffle(shuffled_cards)
        self.n_round = n_round or (len(shuffled_cards) - 1) // n_player

        self.hands: List[Set[Card]] = []
        for player in self.players:
            offset = player * self.n_round
            self.hands.append(set(shuffled_cards[offset: offset + self.n_round]))
        self.remained_hands = [hand.copy() for hand in self.hands]

        # decide trump
        remained_cards = shuffled_cards[self.n_round * n_player:]
        self.trump = remained_cards[0].suit if len(remained_cards) > 0 else None

    @property
    def players(self) -> Iterable[int]:
        return range(self.n_player)

    def predict(self, predictions: List[int]):
        value_check(self.board.predictions is None, 'Predictions have been set')
        value_check(len(predictions) == self.n_player, f'Wrong player count {len(predictions)} (expected {self.n_player})')
        for player, prediction in enumerate(predictions):
            value_check(prediction >= 0, f'prediction of player {player} should be non-negative')

        self.board.predictions = predictions

    def play(self, player: int, card: Card):
        value_check(self.board.predictions is not None, 'Predictions have not been set')
        value_check(player == self.board.cur_player, f'Wrong player {player} (current player is {self.board.cur_player})')
        value_check(card in self.remained_hands[player], f'Card {card} is not in remained hand of player {player}')
        value_check(self.board.can_play_suit(card.suit, self.remained_hands[player]), f'Player {player} should play a {self.board.cur_leading_suit} card')

        assert self.board.cur_round_plays[player] is None
        self.board.cur_round_plays[player] = card
        self.remained_hands[player].remove(card)

        if self.board.is_round_play_finished:
            winner = self._get_winner(self.board.cur_round_play_order, typing.cast(List[Card], self.board.cur_round_plays))
            # pylint: disable=protected-access
            self.board._next_round(leader=winner)

    def _get_winner(self, play_order: List[int], plays: List[Card]) -> int:
        assert set(play_order) == set(self.players)
        assert len(plays) == self.n_player

        for i in play_order:
            if isinstance(plays[i], WizardCard):
                return i

        winner = play_order[0]
        for i in play_order[1:]:
            cur_card = plays[i]
            winner_card = plays[winner]
            if isinstance(winner_card, JesterCard):
                winner = i
                continue
            assert isinstance(winner_card, SuitCard)
            if isinstance(cur_card, JesterCard):
                continue
            assert isinstance(cur_card, SuitCard)
            if cur_card.suit == winner_card.suit:
                if cur_card.standard_rank_index > winner_card.standard_rank_index:
                    winner = i
            elif cur_card.suit == self.trump:
                winner = i
        return winner

    def score(self) -> List[int]:
        value_check(self.board.is_all_finished, 'Unable to score an unfinished game')
        assert self.board.predictions is not None

        prediction_errors = [abs(prediction - winned_round) for prediction, winned_round in zip(self.board.predictions, self.board.winned_rounds())]
        sum_error = sum(prediction_errors)
        scores = [sum_error - self.n_player * error for error in prediction_errors]
        return scores
