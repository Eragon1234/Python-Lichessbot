import logging
import os
import sys
from threading import Thread

import log
from engine import Engine
from game_controller import GameController, Game


def main():
    log.init_logging()

    lichess_token = os.getenv("LICHESS_TOKEN")
    if lichess_token is None:
        logging.error("Missing Lichess token. Please set the environment variable LICHESS_TOKEN to your lichess token.")
        sys.exit(1)

    game = GameController(lichess_token)

    game.on_challenge(lambda challenge: challenge.accept())
    game.on_game_start(start_game)

    game.watch()


def start_game(game: Game):
    engine = Engine(game.start_fen)
    game.on_my_move(engine.move)
    game.on_opponents_move(engine.opponents_move)
    game.watch()


if __name__ == '__main__':
    main()
