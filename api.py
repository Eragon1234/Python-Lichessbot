import json
import os
from collections.abc import Generator

import requests


class LichessBotApiClient:
    """
    LichessBotApi is a class for handling the connection to the lichess bot api
    """
    token = os.environ.get('LICHESS_TOKEN')
    base_url = "https://lichess.org/api"
    s: requests.Session = None

    def __init__(self):
        if self.token is None:
            raise Exception('No token provided')

        s = requests.Session()
        s.headers.update({
            'Authorization': f'Bearer {self.token}'
        })
        self.s = s

    def accept_challenge(self, challenge_id: str) -> None:
        """accepts a challenge with the given challenge_id"""
        self.s.post(f'{self.base_url}/challenge/{challenge_id}/accept')

    def move(self, game_id: str, move: str) -> None:
        """makes a move in the game with the given game_id"""
        self.s.post(f'{self.base_url}/bot/game/{game_id}/move/{move}')

    def stream_events(self) -> Generator[dict, None, None]:
        """streams events from the lichess api"""
        res = self.s.get(f'{self.base_url}/stream/event', stream=True)

        for line in res.iter_lines():
            if not line:
                continue

            # parsing the json response
            event = json.loads(line)

            yield event

    def stream_game(self, game_id: str, *args) -> Generator[dict, None, None]:
        """streams a game with the given game_id"""
        res = self.s.get(f'{self.base_url}/bot/game/stream/{game_id}', stream=True)

        for line in res.iter_lines():
            if not line:
                continue

            # parsing the json response
            event = json.loads(line)

            yield event
