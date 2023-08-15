import logging
import os
import sys

from cache.move_cache import MoveCache
from engine.engine import Engine
from game_controller import GameController, Game
from playercolor import PlayerColor

MISSING_LICHESS_TOKEN = ("Missing Lichess token. "
                         "Please set the environment variable LICHESS_TOKEN.")


def main():
    logging.basicConfig(level=logging.INFO)

    lichess_token = os.getenv("LICHESS_TOKEN")
    if lichess_token is None:
        logging.error(MISSING_LICHESS_TOKEN)
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
    cache = MoveCache(1_000_000)
    engine = Engine(game.start_fen, cache)

    def on_my_move(color: PlayerColor, moves: list[str]):
        move, evaluation = engine.get_best_move(color, moves)
        uci_move = move.uci()
        logging.info("best move %s", uci_move)
        logging.info("evaluation %s\n\n", evaluation)
        game.move(uci_move)

    def on_move(move: str):
        logging.info("moved %s\n\n", move)
        engine.board.move(move)

    game.on_my_move(on_my_move)
    game.on_move(on_move)

    game.watch()


if __name__ == '__main__':
    main()
