from typing import Generic, TypeVar, Iterator

from game.pieces.abstract_piece import AbstractPiece

T = TypeVar('T')


class _Board(Generic[T]):
    def __init__(self, board: list[T]):
        self._board = board

    def __getitem__(self, item: tuple[int, int]) -> T:
        x, y = item
        return self._board[y * 8 + x]

    def __setitem__(self, key: tuple[int, int], value: T):
        x, y = key
        self._board[y * 8 + x] = value

    def __iter__(self) -> Iterator[T]:
        return iter(self._board)

    def __hash__(self) -> int:
        return hash(tuple(self._board))


def position_to_coordinate(position: int) -> tuple[int, int]:
    return position % 8, position // 8


def coordinate_to_position(x: int, y: int) -> int:
    return y * 8 + x
