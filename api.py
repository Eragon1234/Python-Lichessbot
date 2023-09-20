import json
from collections.abc import Iterator

import requests


class LichessBotApiClient:
    """LichessBotApi handles the connection to the lichess bot api"""

    base_url = "https://lichess.org/api"

    def __init__(self, lichess_token: str):
        """Initializes the LichessBotApiClient with the given lichess api token"""
        if lichess_token is None:
            raise ValueError("LichessBotApiClient token cannot be None")

        self.token = lichess_token
        self.s = requests.Session()
        self.s.headers.update({'Authorization': f'Bearer {self.token}'})

    def accept_challenge(self, challenge_id: str) -> None:
        """accepts a challenge with the given challenge_id"""
        self.s.post(f'{self.base_url}/challenge/{challenge_id}/accept')

    def move(self, game_id: str, move: str) -> None:
        """makes a move in the game with the given game_id"""
        self.s.post(f'{self.base_url}/bot/game/{game_id}/move/{move}')

    def _stream(self, url: str) -> Iterator[dict]:
        """Streams the url and yields the response parsed as json"""
        with self.s.get(url, stream=True) as res:
            for line in res.iter_lines():
                if not line:
                    continue

                yield json.loads(line)

    def stream_events(self) -> Iterator[dict]:
        """streams events from the lichess api"""
        return self._stream(f'{self.base_url}/stream/event')

    def stream_game(self, game_id: str) -> Iterator[dict]:
        """streams a game with the given game_id"""
        return self._stream(f'{self.base_url}/bot/game/stream/{game_id}')
