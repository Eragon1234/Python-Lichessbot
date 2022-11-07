from multiprocessing import Process
import json

import requests


class GameController:
    """
    handles the connection to the lichess bot api with an event emitter
    """
    # our lichess token for access to the bot api
    token = ''

    # our dictionary for storing the event functions
    events: dict[str, list[callable]] = {}

    # the color to be played by the bot
    color = 'white'

    def __init__(self):
        # creating a requests session to always send the Authorization header as the lichess token at every request
        s = requests.Session()
        s.headers.update({
            'Authorization': 'Bearer ' + self.token,
        })
        self.s = s

    def watch(self):
        """
        subscribes to the lichess api to watch for events as challenge, gameStart etc. and emits the belonging events
        """

        # starting a stream of events from lichess
        res = self.s.get('https://lichess.org/api/stream/event', stream=True)

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

    def on(self, event, fn):
        """ adds functions to be called on the mentioned incoming events

        Args:
            event (string): the event to be handled
            fn (function): the function to be assigned to the passed event
        """

        # if event doesn't already exist create empty array at key event
        if event not in self.events.keys():
            self.events[event] = []

        # append event to event array
        self.events[event].append(fn)

    def emit(self, event, *params):
        """ calls the assigned functions to the passed event with the given parameters

        Args:
            event (string): the event for whom the assigned functions to be called
            *params: the parameters to be passed to the assigned functions
        """

        # checking if event exists
        if event not in self.events.keys():
            return

        # calling every function in the array at the key event with the passed parameters
        for event in self.events[event]:
            Process(target=event, args=params).start()

    def move(self, game_id, move):
        """ moves the passed move

        Args:
            game_id (string): the gameId for the game in which the move should be played
            move (UCIMove): the move to play in UCI notation
        """
        self.s.post(f'https://lichess.org/api/bot/game/{game_id}/move/{move}')

    def accept_challenge(self, challenge_id, *args):
        """ accepts the challenge with the passed challengeId

        Args:
            challenge_id (string): the challengeId of the challenge to be accepted
        """
        self.s.post(f'https://lichess.org/api/challenge/{challenge_id}/accept')

    def stream_game(self, game_id, *args):
        """ subscribing to the stream of events for the game with the passed gameId

        Args:
            game_id (string): the gameId of the game to be subscribed to
        """

        # subscribing to the stream
        res = self.s.get(f'https://lichess.org/api/bot/game/stream/{game_id}', stream=True)
        # handling every incoming event
        for line in res.iter_lines():
            if line:
                # parsing the json response
                event = json.loads(line)
                # checking if there is an object with the key of 'state' in the response
                if 'state' in event.keys():
                    # getting the moves from the response
                    moves = event['state']['moves']

                    # setting the my_move property to true if I'm white else to black
                    if self.color == 'white':
                        my_move = True
                    else:
                        my_move = False
                else:
                    # getting the moves from the response
                    moves = event['moves']

                    # checking if it's whites Move by counting the number of plies
                    if (moves.count(" ") % 2) == 1:
                        my_move = True
                    else:
                        my_move = False

                    # inverting my_move if I'm black
                    if self.color == 'black':
                        my_move = not my_move

                # checking if it's my_move
                if my_move:
                    # parsing the moves as an array
                    moves = moves.split(" ")
                    # checking if last move is from my opponent

                    if len(moves) >= 1 and len(moves[-1]) >= 4:
                        # sending the opponents_move event with the move as an argument
                        move = moves[-1]
                        self.emit('opponents_move', move)

                    # sending the my_move event with the gameId, the moves and the move function as arguments
                    self.emit('my_move', game_id, self.color, moves, self.move)
