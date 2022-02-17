# importing the GameController for handling the connetion to the Lichess API
from GameController import GameController

# importing our Engine
from Engine import Engine

# initializing our GameController
game = GameController()

# justa accepting challenges and streaming games without further processing
game.on('challenge', game.acceptChallenge)
game.on('gameStart', game.streamGame)

# initializing our Engine
engine = Engine()

# adding the methods of the engine to handle the engines turn and the incoming moves of the opponent
game.on('myMove', engine.move)
game.on('opponentsMove', engine.opponentsMove)

# starting to watch for events
game.watch()