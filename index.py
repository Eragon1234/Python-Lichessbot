import GameController
game = GameController.GameController()

game.on('challenge', game.acceptChallenge)
game.on('gameStart', game.streamGame)

def move(gameId, moves, moveFn):
    moveFn(gameId, "d7d5")

game.on('myMove', move)

game.watch()