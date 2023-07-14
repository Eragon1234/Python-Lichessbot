import logging
import os
import sys

import log
from engine import Engine
from game_controller import GameController


def main():
    log.init_logging()

    lichess_token = os.getenv("LICHESS_TOKEN")
    if lichess_token is None:
        logging.error("Missing Lichess token. Please set the environment variable LICHESS_TOKEN to your lichess token.")
        sys.exit(1)

    game = GameController(lichess_token)

    game.on('challenge', game.accept_challenge)
    game.on('game_start', game.stream_game)

    engine = Engine()

    game.on('my_move', engine.move)
    game.on('opponents_move', engine.opponents_move)

    game.watch()


if __name__ == '__main__':
    main()
