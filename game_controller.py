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
        self.color = None

    def watch(self) -> typing.NoReturn:
        """subscribes to the lichess api and emits the events"""
        for event in self.client.stream_events():
            if event['type'] == 'challenge':
                challenge_id = event['challenge']['id']

                self.emitter.emit('challenge', challenge_id, self.client.accept_challenge)
            elif event['type'] == 'gameStart':
                game_id = event['game']['gameId']
                self.color = PlayerColor(event['game']['color'])
                opponent = event['game']['opponent']

                self.emitter.emit('game_start', game_id, opponent, self.stream_game)

    def on(self, event: str, fn: typing.Callable[[str, ...], None]) -> None:
        """ adds functions to be called on the mentioned incoming events

        Args
            event (str): the event to be handled
            fn (callable): the function to be assigned to the passed event
        """
        self.emitter.on(event, fn)

    def stream_game(self, game_id: str, *args) -> None:
        """ Subscribes to the events for the game with and emits the events

        Args:
            game_id (str): the gameId of the game to be subscribed to
        """
        for event in self.client.stream_game(game_id):
            if 'state' in event.keys():
                moves = event['state']['moves']
            else:
                moves = event['moves']

            moves = moves.split(" ")

            # if the number of plies is even, it's white's move
            whites_move = (len(moves) % 2) == 1 or moves[0] == ''

            my_move = whites_move == (self.color is PlayerColor.White)

            if my_move:
                # if there is a move before the current one,
                # it's the opponent's move
                if len(moves) >= 1 and moves[-1] != '':
                    move = moves[-1]
                    self.emitter.emit('opponents_move', move)

                move_callback = partial(self.client.move, game_id)
                self.emitter.emit('my_move', self.color.value, moves, move_callback)

    def accept_challenge(self, challenge_id: str, *args) -> None:
        """Accepts the challenge with the passed challenge_id

        Args:
            challenge_id (str): the id of the challenge to be accepted
        """
        self.client.accept_challenge(challenge_id)
