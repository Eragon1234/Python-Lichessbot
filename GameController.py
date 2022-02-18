import requests
import json

class GameController:
    """
    handles the connection to the lichess bot api with an event emmiter
    """
    # our lichess token for access to the bot api
    token = 'lip_2KigTbBKsXIeBFcnCnWk'

    # our dictionary for storing the event functions
    events = {}

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
            if line:
                # parsing the json response
                event = json.loads(line)

                # checking if the event type is challenge
                if event['type'] == 'challenge':
                    # getting the challengeId and the challenger
                    challengeId = event['challenge']['id']

                    # throwing the challenge event with the challengeId, the challenger and the function to accept the challenge as params
                    self.emit('challenge', challengeId, self.acceptChallenge)

                # checking if the event type is gameStart
                elif event['type'] == 'gameStart':
                    
                    # getting the gameId, the color the engine is playing and data about the opponent
                    gameId = event['game']['gameId']
                    self.color = event['game']['color']
                    opponent = event['game']['opponent']

                    # throwing the gameStart event with the gameId, the opponent and the function to start streaming the game
                    self.emit('gameStart', gameId, opponent, self.streamGame)

    def on(self, event, fn):
        """ adds functions to be called on the mentioned incoming events

        Args:
            event (string): the event to be handled
            fn (function): the function to be assigned to the passed event
        """

        # if event already exists append function
        if event in self.events.keys():
            self.events[event].append(fn)
        
        # else create a new array for the functions with the event name as the key
        else:
            self.events[event] = []
            self.events[event].append(fn) 

    def emit(self, event, *params):
        """ calls the assigned functions to the passed event with the given parameters

        Args:
            event (string): the event for whom the assigned functions to be called
            *params: the parameters to be passed to the assigned functions
        """

        # checking if event exists
        if event in self.events.keys():
            # calling every function in the array at the key event with the passed parameters
            for event in self.events[event]:
                event(*params)

    def move(self, gameId, move):
        """ moves the passed move

        Args:
            gameId (string): the gameId for the game in which the move should be played
            move (UCIMove): the move to play in UCI notation
        """
        r = self.s.post(f'https://lichess.org/api/bot/game/{gameId}/move/{move}')
    
    def acceptChallenge(self, challengeId, *params):
        """ accepts the challenge with the passed challengeId

        Args:
            challengeId (string): the challengeId of the challenge to be accepted
        """
        self.s.post(f'https://lichess.org/api/challenge/{challengeId}/accept')
    
    def streamGame(self, gameId, *params):
        """ subscribing to the strem of events for the game with the passed gameId

        Args:
            gameId (string): the gameId of the game to be subscribed to
        """

        # subscribing to the stream
        res = self.s.get(f'https://lichess.org/api/bot/game/stream/{gameId}', stream=True)
        # handling every incoming event
        for line in res.iter_lines():
            if line:
                # parsing the json response
                event = json.loads(line)
                # checking if there is an object with the key of 'state' in the response
                if 'state' in event.keys():
                    # getting the moves from the response
                    moves = event['state']['moves']

                    # setting the myMove property to true if I'm white else to black
                    if self.color == 'white':
                        myMove = True
                    else:
                        myMove = False
                else:
                    # getting the moves from the response
                    moves = event['moves']

                    # checking if it's whites Move by counting the number of plies
                    if (moves.count(" ") % 2) == 1:
                        myMove = True
                    else:
                        myMove = False
                    
                    # inverting myMove if I'm black
                    if self.color == 'black':
                        myMove = not myMove
                
                # checking if it's myMove
                if myMove:
                    # parsing the moves as an array
                    moves = moves.split(" ")
                    # checking if last move is from my opponent
                    
                    if len(moves) >= 1 and len(moves[-1]) >= 4:
                        # sending the opponentsMove event with the move as an argument
                        move = moves[-1]
                        print("opponents turn")
                        print("opponent moved:", move)
                        self.emit('opponentsMove', move)
                        print("------------------------------------------------------------------------------------------------")
                    
                    # sending the myMove event with the gameId, the moves and the move function as arguments
                    print("myMove")
                    self.emit('myMove', gameId, self.color, moves, self.move)
                    print("------------------------------------------------------------------------------------------------")