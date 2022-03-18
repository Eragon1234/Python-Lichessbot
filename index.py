# importing the GameController for handling the connection to the Lichess API
# importing our Engine
from engine import Engine
from game_controller import GameController

# initializing our GameController
game = GameController()

# justa accepting challenges and streaming games without further processing
game.on('challenge', game.accept_challenge)
game.on('gameStart', game.stream_game)

# initializing our Engine
engine = Engine()

# adding the methods of the engine to handle the engines turn and the incoming moves of the opponent
game.on('myMove', engine.move)
game.on('opponents_move', engine.opponents_move)

# starting to watch for events
game.watch()
