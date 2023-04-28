import abc


class TestMoveInterface(abc.ABC):
    @abc.abstractmethod
    def move(self, move: str):
        pass

    @abc.abstractmethod
    def unmove(self, move: str):
        pass


class TestMove:
    def __init__(self, board: TestMoveInterface, move: str):
        self.board = board
        self.move = move

    def __enter__(self):
        self.board.move(self.move)
        return self.board

    def __exit__(self, *args):
        self.board.unmove(self.move)
