from typing import Iterator

from game.piece import Piece, Color, PieceType


class _ChessBoard:
    def __init__(self, board: list[Piece], turn: Color,
                 castling_rights: set[str], en_passant: str, halfmove_clock: int,
                 fullmove_number: int):
        self._board = board

        self.turn = turn
        self.castling_rights = castling_rights
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

    def __getitem__(self, item: tuple[int, int]) -> Piece:
        return self._board[item[1] * 8 + item[0]]

    def __setitem__(self, key: tuple[int, int], value: Piece):
        value.move_to(key)
        self._board[key[1] * 8 + key[0]] = value

    def __iter__(self) -> Iterator[Piece]:
        return iter(self._board)

    def iter_rows(self) -> Iterator[list[Piece]]:
        """
        Iterate over the rows of the board.
        The rows are a8-h8, a7-h7, ..., a1-h1
        """
        for i in reversed(range(8)):
            yield reversed(self._board[i * 8:i * 8 + 8])

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

        turn = Color.WHITE if fen_parts[1] == "w" else Color.BLACK
        castling_rights = set(fen_parts[2])
        castling_rights.discard("-")
        en_passant = fen_parts[3]
        halfmove_clock = int(fen_parts[4])
        fullmove_number = int(fen_parts[5])

        return cls(board, turn, castling_rights, en_passant,
                   halfmove_clock, fullmove_number)

    def fen(self) -> str:
        rows = []
        for row in self.iter_rows():
            empty_count = 0
            row_fen = ""
            for piece in row:
                if piece.type == PieceType.EMPTY:
                    empty_count += 1
                    continue

                if empty_count > 0:
                    row_fen += str(empty_count)
                    empty_count = 0
                row_fen += piece.fen()

            if empty_count > 0:
                row_fen += str(empty_count)

            rows.append(row_fen)

        fen = "/".join(rows)

        castling_rights = "".join(sorted(self.castling_rights))
        if castling_rights == "":
            castling_rights = "-"

        return (f"{fen} {'w' if self.turn is Color.WHITE else 'b'} "
                f"{castling_rights} {self.en_passant} "
                f"{self.halfmove_clock} {self.fullmove_number}")

    def material_difference(self) -> int:
        return sum(piece.value for piece in self)

    def color_at(self, position: tuple[int, int]) -> Color:
        return self[position].color

    def pop(self, position: tuple[int, int]) -> Piece:
        piece = self[position]
        self[position] = Piece(PieceType.EMPTY, Color.EMPTY)
        return piece


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
