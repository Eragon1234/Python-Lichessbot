from GameController import GameController
game = GameController()

game.on('challenge', game.acceptChallenge)
game.on('gameStart', game.streamGame)

# Add a function to the event to move
# game.on('myMove', move)

game.watch()