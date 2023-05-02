import os

from engine import Engine
from game_controller import GameController

lichess_token = os.getenv("LICHESS_TOKEN")

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
