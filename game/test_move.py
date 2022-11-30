class TestMove:
    def __init__(self, board, move: str):
        self.board = board
        self.move = move

    def __enter__(self):
        self.board.move(self.move)
        return self.board

    def __exit__(self, *args):
        self.board.unmove(self.move)
