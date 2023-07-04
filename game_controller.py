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
        """subscribes to the lichess api to watch for events as a challenge, gameStart etc. and emits the belonging
        events"""
        for event in self.client.stream_events():
            # checking if the event type is a challenge
            if event['type'] == 'challenge':
                # getting the challenge_id and the challenger
                challenge_id = event['challenge']['id']

                # throwing the challenge event with the challenge_id, the challenger and the function to accept
                # the challenge as params
                self.emitter.emit('challenge', challenge_id, self.client.accept_challenge)

            # checking if the event type is gameStart
            elif event['type'] == 'gameStart':

                # getting the game_id, the color the engine is playing and data about the opponent
                game_id = event['game']['gameId']
                self.color = PlayerColor(event['game']['color'])
                opponent = event['game']['opponent']

                # throwing the gameStart event with the game_id, the opponent and the function to start streaming
                # the game
                self.emitter.emit('game_start', game_id, opponent, self.stream_game)

    def on(self, event: str, fn: typing.Callable[[str, ...], None]) -> None:
        """ adds functions to be called on the mentioned incoming events

        Args:
            event (str): the event to be handled
            fn (callable): the function to be assigned to the passed event
        """
        self.emitter.on(event, fn)

    def stream_game(self, game_id: str, *args) -> None:
        """ Subscribing to the stream of events for the game with the passed gameId

        Args:
            game_id (str): the gameId of the game to be subscribed to
        """
        for event in self.client.stream_game(game_id):
            # checking if there is an object with the key of 'state' in the response
            if 'state' in event.keys():
                # getting the moves from the response
                moves = event['state']['moves']
            else:
                # getting the moves from the response
                moves = event['moves']

            moves = moves.split(" ")

            # checking if it's whites Move by counting the number of plies
            my_move = (len(moves) % 2) == 0 or moves[0] == ''

            # inverting my_move if I'm black
            if self.color is PlayerColor.Black:
                my_move = not my_move

            # checking if it's my_move
            if my_move:
                # checking if the last move is from my opponent
                if len(moves) >= 1 and moves[-1] != '':
                    # sending the opponents_move event with the move as an argument
                    move = moves[-1]
                    self.emitter.emit('opponents_move', move)

                # sending the my_move event with the gameId, the moves and the move function as arguments
                move_callback = partial(self.client.move, game_id)
                self.emitter.emit('my_move', self.color.value, moves, move_callback)

    def accept_challenge(self, challenge_id: str, *args) -> None:
        """Accepts the challenge with the passed challenge_id

        Args:
            challenge_id (str): the id of the challenge to be accepted
        """
        self.client.accept_challenge(challenge_id)
