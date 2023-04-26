import json
import os
import typing

import requests


class GameController:
    """handles the connection to the lichess bot api with an event emitter"""

    # the base url for all api requests
    base_url = "https://lichess.org/api"

    # our lichess token for access to the bot api
    token = os.environ.get('LICHESS_TOKEN')

    # our dictionary for storing the event functions
    events: dict[str, list[callable]] = {}

    # the color to be played by the bot
    color = 'white'

    def __init__(self):
        if self.token is None:
            raise Exception('No token provided')

        # creating a requests session to always send the Authorization header as the lichess token at every request
        s = requests.Session()
        s.headers.update({
            'Authorization': 'Bearer ' + self.token,
        })
        self.s = s

    def watch(self) -> None:
        """subscribes to the lichess api to watch for events as a challenge, gameStart etc. and emits the belonging
        events"""
        # starting a stream of events from lichess
        res = self.s.get(f'{self.base_url}/stream/event', stream=True)

        # handling every incoming event
        for line in res.iter_lines():
            if not line:
                continue

            # parsing the json response
            event = json.loads(line)

            # checking if the event type is challenge
            if event['type'] == 'challenge':
                # getting the challenge_id and the challenger
                challenge_id = event['challenge']['id']

                # throwing the challenge event with the challenge_id, the challenger and the function to accept
                # the challenge as params
                self.emit('challenge', challenge_id, self.accept_challenge)

            # checking if the event type is gameStart
            elif event['type'] == 'gameStart':

                # getting the game_id, the color the engine is playing and data about the opponent
                game_id = event['game']['gameId']
                self.color = event['game']['color']
                opponent = event['game']['opponent']

                # throwing the gameStart event with the game_id, the opponent and the function to start streaming
                # the game
                self.emit('game_start', game_id, opponent, self.stream_game)

    def on(self, event: str, fn: typing.Callable[[str, ...], None]) -> None:
        """ adds functions to be called on the mentioned incoming events

        Args:
            event (str): the event to be handled
            fn (callable): the function to be assigned to the passed event
        """
        # if the event doesn't already exist create an empty array at key event
        if event not in self.events:
            self.events[event] = []

        # append event to an event array
        self.events[event].append(fn)

    def emit(self, event: str, *params) -> None:
        """ calls the assigned functions to the passed event with the given parameters

        Args:
            event (str): the event for whom the assigned functions to be called
            *params: the parameters to be passed to the assigned functions
        """
        # checking if event exists
        if event not in self.events:
            return

        # calling every function in the array at the key event with the passed parameters
        for e in self.events[event]:
            e(*params)

    def move(self, game_id: str, move: str) -> None:
        """ moves the passed move

        Args:
            game_id (str): the gameId for the game in which the move should be played
            move (str): the move to play in UCI notation
        """
        self.s.post(f'{self.base_url}/bot/game/{game_id}/move/{move}')

    def accept_challenge(self, challenge_id: str, *args) -> None:
        """ accepts the challenge with the passed challengeId

        Args:
            challenge_id (str): the challengeId of the challenge to be accepted
        """
        self.s.post(f'{self.base_url}/challenge/{challenge_id}/accept')

    def stream_game(self, game_id: str, *args) -> None:
        """ subscribing to the stream of events for the game with the passed gameId

        Args:
            game_id (str): the gameId of the game to be subscribed to
        """
        # subscribing to the stream
        res = self.s.get(f'{self.base_url}/bot/game/stream/{game_id}', stream=True)
        # handling every incoming event
        for line in res.iter_lines():
            if not line:
                continue

            # parsing the json response
            event = json.loads(line)
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
            if self.color == 'black':
                my_move = not my_move

            # checking if it's my_move
            if my_move:
                # checking if the last move is from my opponent
                if len(moves) >= 1 and moves[-1] != '':
                    # sending the opponents_move event with the move as an argument
                    move = moves[-1]
                    self.emit('opponents_move', move)

                # sending the my_move event with the gameId, the moves and the move function as arguments
                self.emit('my_move', game_id, self.color, moves, self.move)
