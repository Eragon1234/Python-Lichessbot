class TestMove:
    def __init__(self, board, move):
        self.board = board
        self.move = move

    def __enter__(self):
        self.board.move(self.move)
        return self.board

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.board.unmove(self.move)