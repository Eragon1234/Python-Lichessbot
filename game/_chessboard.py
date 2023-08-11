from typing import Iterator

from game.piece import Piece, Color, PieceType


class _ChessBoard:
    def __init__(self, board: list[Piece], white_to_move: bool,
                 castling_rights: str, en_passant: str, halfmove_clock: int,
                 fullmove_number: int):
        self._board = board

        self.white_to_move = white_to_move
        self.castling_rights = castling_rights
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

    def __getitem__(self, item: tuple[int, int]) -> Piece:
        x, y = item
        return self._board[y * 8 + x]

    def __setitem__(self, key: tuple[int, int], value: Piece):
        x, y = key
        self._board[y * 8 + x] = value

    def __iter__(self) -> Iterator[Piece]:
        return iter(self._board)

    def __hash__(self) -> int:
        return hash(tuple(self._board))

    @classmethod
    def from_fen(cls, fen: str) -> '_ChessBoard':
        board = []
        fen_parts = fen.split()

        position = fen_parts[0].split("/")
        for row in position:
            for char in row:
                if char.isdigit():
                    n = int(char)
                    board.extend(Piece(PieceType.EMPTY, Color.EMPTY) for _ in range(n))
                    continue

                board.append(Piece.from_fen(char))

        board.reverse()

        white_to_move = fen_parts[1] == "w"
        castling_rights = fen_parts[2]
        en_passant = fen_parts[3]
        halfmove_clock = int(fen_parts[4])
        fullmove_number = int(fen_parts[5])

        return cls(board, white_to_move, castling_rights, en_passant,
                   halfmove_clock, fullmove_number)

    def material_difference(self) -> int:
        return sum(piece.value for piece in self)

    def color_at(self, position: tuple[int, int]) -> Color:
        return self[position].color


def position_to_coordinate(position: int) -> tuple[int, int]:
    """
    Convert an index in a 1d list to its equivalent in a 8x8 2d list

    Args:
        position: the index of the item in the 1d list

    Returns:
        returns the x and y coordinate of the position in a 8x8 2d list
    """
    return position % 8, position // 8


def coordinate_to_position(x: int, y: int) -> int:
    """
    Convert a coordinate in a 8x8 2d list to its equivalent in a 1d list

    Args:
        x: the x coordinate of the position in a 8x8 2d list
        y: the y coordinate of the position in a 8x8 2d list

    Returns:
        returns the index of the item in the 1d list
    """
    return y * 8 + x
