from GameController import GameController
from Engine import Engine
game = GameController()

game.on('challenge', game.acceptChallenge)
game.on('gameStart', game.streamGame)

engine = Engine()
game.on('myMove', engine.move)
game.on('opponentsMove', engine.opponentsMove)

game.watch()