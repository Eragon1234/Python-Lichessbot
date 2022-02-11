from operator import truediv
import requests
import json

class GameController:
    token = 'lip_2KigTbBKsXIeBFcnCnWk'
    events = {}

    def __init__(self):
        s = requests.Session()
        s.headers.update({
            'Authorization': 'Bearer ' + self.token,
        })
        self.s = s

    def watch(self):
        res = self.s.get('https://lichess.org/api/stream/event', stream=True)

        for line in res.iter_lines():
            if line:
                event = json.loads(line)
                if event['type'] == 'challenge':
                    challengeId = event['challenge']['id']
                    self.emit('challenge', challengeId, self.acceptChallenge)
                elif event['type'] == 'gameStart':
                    gameId = event['game']['gameId']
                    self.color = event['game']['color']
                    self.emit('gameStart', gameId, self.streamGame)

    def on(self, event, fn):
        if event in self.events.keys():
            self.events[event].append(fn)
        else:
            self.events[event] = []
            self.events[event].append(fn) 

    def emit(self, event, *params):
        if event in self.events.keys():
            for event in self.events[event]:
                event(*params)

    def move(self, gameId, move):
        s = f'https://lichess.org/api/bot/game/{gameId}/move/{move}'
        print(s)
        r = self.s.post(f'https://lichess.org/api/bot/game/{gameId}/move/{move}')
        print(r.content)
    
    def acceptChallenge(self, challengeId, *other):
        self.s.post(f'https://lichess.org/api/challenge/{challengeId}/accept')
    
    def streamGame(self, gameId, *other):
        res = self.s.get(f'https://lichess.org/api/bot/game/stream/{gameId}', stream=True)
        for line in res.iter_lines():
            if line:
                event = json.loads(line)
                if 'state' in event.keys():
                    moves = event['state']['moves']
                    if self.color == 'white':
                        myMove = True
                    else:
                        myMove = False
                else:
                    moves = event['moves']
                    if (moves.count(" ") % 2) == 1:
                        myMove = True
                    else:
                        myMove = False
                    
                    if self.color == 'black':
                        myMove = not myMove

                if myMove:
                    self.emit('myMove', gameId, moves, self.move)
                else:
                    continue
                    