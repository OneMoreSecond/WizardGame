import argparse
from typing import List

from game import StandardGame
import strategy
from strategy import Strategy
from helper import print_separator


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', dest='strategies', nargs='+', default=['human'] * 4)
    return parser


def main(args):
    game = StandardGame(n_player=len(args.strategies))
    agents: List[Strategy] = [getattr(strategy, name.title() + 'Strategy')(i, game.trump, game.hands[i]) for i, name in enumerate(args.strategies)]
    predictions = [agent.prediction for agent in agents]
    game.predict(predictions)

    while not game.board.is_all_finished:
        while game.board.cur_player is not None:
            play = agents[game.board.cur_player].play(game.board)
            game.play(game.board.cur_player, play)

    scores = game.score()
    print_separator()
    print('Scores:')
    for i, score in enumerate(scores):
        print(f'Player {i}: {score}')


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)
