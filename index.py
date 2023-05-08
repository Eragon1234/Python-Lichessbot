import logging
import os

from engine import Engine
from formatter import MyFormatter
from game_controller import GameController


def main():
    logging.basicConfig(level=logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(MyFormatter())
    logging.getLogger().handlers.clear()
    logging.getLogger().addHandler(stream_handler)

    lichess_token = os.getenv("LICHESS_TOKEN")
    if lichess_token is None:
        logging.error("No lichess token found. Please set the environment variable LICHESS_TOKEN to your lichess token.")
        exit(1)

    # initializing our GameController
    game = GameController(lichess_token)

    # just accepting challenges and streaming games without further processing
    game.on('challenge', game.accept_challenge)
    game.on('game_start', game.stream_game)

    # initializing our Engine
    engine = Engine()

    # adding the methods of the engine to handle the engines turn and the incoming moves of the opponent
    game.on('my_move', engine.move)
    game.on('opponents_move', engine.opponents_move)

    # starting to watch for events
    game.watch()


if __name__ == '__main__':
    main()
