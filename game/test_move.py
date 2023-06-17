from typing import TypeVar, Generic, Protocol


class TestMoveInterface(Protocol):
    def move(self, move: str):
        pass

    def unmove(self, move: str):
        pass


T = TypeVar("T", bound=TestMoveInterface)


class TestMove(Generic[T]):
    def __init__(self, board: T, move: str):
        self.board = board
        self.move = move

    def __enter__(self) -> T:
        self.board.move(self.move)
        return self.board

    def __exit__(self, *args):
        self.board.unmove(self.move)
