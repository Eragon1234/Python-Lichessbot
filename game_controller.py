import typing
from functools import partial

from api import LichessBotApiClient
from event_emitter import EventEmitter
from playercolor import PlayerColor


class GameController:
    """handles the connection to the lichess bot api with an event emitter"""

    def __init__(self, token: str):
        self.client = LichessBotApiClient(token)
        self.emitter = EventEmitter()

    def watch(self) -> typing.NoReturn:
        """subscribes to the lichess api and emits the events"""
        for event in self.client.stream_events():
            if event['type'] == 'challenge':
                challenge_id = event['challenge']['id']

                self.emit_challenge(challenge_id)
            elif event['type'] == 'gameStart':
                game_id = event['game']['gameId']
                color = event['game']['color']
                opponent = event['game']['opponent']['id']
                initial_fen = event['game']['fen']

                self.emit_game_start(game_id, color, opponent, initial_fen)

    def emit_challenge(self, challenge_id: str):
        accept_challenge = partial(self.accept_challenge, challenge_id)
        challenge = Challenge(challenge_id, accept_challenge)

        self.emitter.emit('challenge', challenge)

    def emit_game_start(self, game_id: str, color: str,
                        opponent: str, initial_fen: str):
        color = PlayerColor(color)

        game = Game(self.client, color, game_id, initial_fen, opponent)

        self.emitter.emit('game_start', game)

    def on_challenge(self, fn: typing.Callable[["Challenge"], None]):
        """adds a function to be called on an incoming challenge"""
        self.emitter.on('challenge', fn)

    def on_game_start(self, fn: typing.Callable[["Game"], None]):
        """adds a function to be called on an incoming game start"""
        self.emitter.on('game_start', fn)

    def accept_challenge(self, challenge_id: str, *args) -> None:
        """
        Accepts the challenge with the passed challenge_id

        Args:
            challenge_id (str): the id of the challenge to be accepted
        """
        self.client.accept_challenge(challenge_id)


class Challenge:
    """Represents a challenge"""

    def __init__(self, challenge_id: str, accept: typing.Callable[[], None]):
        self.challenge_id = challenge_id
        self.accept = accept


class Game:
    """Represents a game"""

    def __init__(self, client: LichessBotApiClient, color: PlayerColor,
                 game_id: str, start_fen: str, opponent: str):
        self.client = client
        self.color = color
        self.game_id = game_id
        self.opponent = opponent
        self.start_fen = start_fen

        self.emitter = EventEmitter()

    def on_my_move(self, fn: typing.Callable[[PlayerColor, list[str]], None]):
        self.emitter.on('my_move', fn)

    def on_move(self, fn: typing.Callable[[str], None]):
        self.emitter.on('move', fn)

    def watch(self):
        for event in self.client.stream_game(self.game_id):
            if event['type'] == 'gameFull':
                state = event['state']
            elif event['type'] == 'gameState':
                state = event
            else:
                continue

            moves = state['moves']

            moves = moves.split(" ")

            # if the number of plies is even, it's white's move
            whites_move = (len(moves) % 2) == 0 or moves[0] == ''

            my_move = whites_move == (self.color is PlayerColor.White)

            if len(moves) > 0 and moves[-1] != '':
                self.emitter.emit('move', moves[-1])

            if my_move:
                self.emitter.emit('my_move', self.color, moves)

    def move(self, move: str):
        self.client.move(self.game_id, move)
