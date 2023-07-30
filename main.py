import logging
import os
import sys

import log
from engine import Engine
from game_controller import GameController, Game
from playercolor import PlayerColor


def main():
    log.init_logging()

    lichess_token = os.getenv("LICHESS_TOKEN")
    if lichess_token is None:
        logging.error("Missing Lichess token. Please set the environment variable LICHESS_TOKEN to your lichess token.")
        sys.exit(1)

    game = GameController(lichess_token)

    game.on_challenge(lambda challenge: challenge.accept())
    game.on_game_start(start_game)

    try:
        game.watch()
    except KeyboardInterrupt:
        logging.info("Exiting")


def start_game(game: Game):
    logging.info("start fen: %s", game.start_fen)
    engine = Engine(game.start_fen)

    def on_my_move(color: PlayerColor, moves: list[str]):
        logging.info("my move")
        move, evaluation = engine.get_best_move(color, moves)
        logging.info("moved %s", move)
        logging.info("evaluation %s", evaluation)
        engine.board.move(move)
        game.move(move)

    def on_opponents_move(move: str):
        logging.info("opponent moved %s", move)
        engine.board.move(move)

    game.on_my_move(on_my_move)
    game.on_opponents_move(on_opponents_move)

    game.watch()


if __name__ == '__main__':
    main()
