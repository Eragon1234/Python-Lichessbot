import copy
from collections.abc import Iterator
from typing import Optional

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.piece.color import Color
from game.piece.piece_type import PieceType

coordinates = [Coordinate.from_index(i) for i in range(64)]


class Board:
    def __init__(self, board: list[PieceType], turn: Color,
                 castling_rights: CastlingRights,
                 en_passant: Optional[Coordinate],
                 halfmove_clock: int, fullmove_number: int):
        self._boards: dict[PieceType, int] = {t: 0 for t in PieceType}

        for i, piece in enumerate(board):
            self._set_type(i, piece)

        self.turn = turn
        self.castling_rights = castling_rights
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

    def __hash__(self) -> int:
        return hash(self.fen())

    def clone(self) -> 'Board':
        return copy.deepcopy(self)

    def is_type(self, i: int, t: PieceType):
        return self._boards[t] & (1 << i)

    def __getitem__(self, item: Coordinate) -> PieceType:
        return self._get_type(item.value)

    def _get_type(self, i: int) -> PieceType:
        piece_type = PieceType(0)
        for t, b in self._boards.items():
            if not b & (1 << i):
                continue
            piece_type |= t
        return piece_type

    def __setitem__(self, key: Coordinate, value: PieceType):
        self._set_type(key.value, value)

    def _set_type(self, i: int, piece_type: PieceType):
        self._clear_bits(i)
        for t in piece_type:
            self._boards[t] |= 1 << i

    def _clear_bits(self, i: int) -> None:
        mask = ~(1 << i)
        for t in self._boards:
            self._boards[t] &= mask

    def __iter__(self) -> Iterator[PieceType]:
        return (self._get_type(i) for i in range(64))

    def iter_rows(self) -> Iterator[list[PieceType]]:
        """
        Iterate over the rows of the board.
        The rows are a8-h8, a7-h7, ..., a1-h1
        """
        for i in reversed(range(8)):
            yield list(self[Coordinate(j, i)] for j in reversed(range(8)))

    @classmethod
    def from_fen(cls, fen: str) -> 'Board':
        board = []
        fen_parts = fen.split()

        position = fen_parts[0].split("/")
        for row in position:
            for char in row:
                if char.isdigit():
                    n = int(char)
                    board.extend(PieceType.EMPTY for _ in range(n))
                    continue

                board.append(PieceType.from_fen(char))

        board.reverse()

        turn = Color.WHITE if fen_parts[1] == "w" else Color.BLACK
        castling_rights = CastlingRights.NONE
        if fen_parts[2] != "-":
            for char in fen_parts[2]:
                if char == "K":
                    castling_rights |= CastlingRights.WHITE_KING
                elif char == "Q":
                    castling_rights |= CastlingRights.WHITE_QUEEN
                elif char == "k":
                    castling_rights |= CastlingRights.BLACK_KING
                elif char == "q":
                    castling_rights |= CastlingRights.BLACK_QUEEN

        en_passant = None
        if fen_parts[3] != "-":
            en_passant = Coordinate.from_uci(fen_parts[3])

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

        castling_rights = ""
        if CastlingRights.WHITE_KING in self.castling_rights:
            castling_rights += "K"
        if CastlingRights.WHITE_QUEEN in self.castling_rights:
            castling_rights += "Q"
        if CastlingRights.BLACK_KING in self.castling_rights:
            castling_rights += "k"
        if CastlingRights.BLACK_QUEEN in self.castling_rights:
            castling_rights += "q"

        if castling_rights == "":
            castling_rights = "-"

        en_passant = "-" if self.en_passant is None else self.en_passant.uci()

        return (f"{fen} {'w' if self.turn is Color.WHITE else 'b'} "
                f"{castling_rights} {en_passant} "
                f"{self.halfmove_clock} {self.fullmove_number}")

    def material_difference(self) -> int:
        return sum(piece.value for piece in self)

    def color_at(self, position: Coordinate) -> Color:
        if position[0] < 0 or position[0] > 7 or \
                position[1] < 0 or position[1] > 7:
            return Color.NONE
        for color in PieceType.COLORS:
            if self.is_type(position.value, color):
                return Color.WHITE if color is PieceType.WHITE else Color.BLACK
        return Color.EMPTY

    def pop(self, position: Coordinate) -> PieceType:
        piece = self[position]
        self[position] = PieceType.EMPTY
        return piece

    def do_move(self, start: Coordinate, target: Coordinate) -> PieceType:
        """
        Removes the piece at the start field and moves it to the end field.
        If there is a piece at the end field, it is removed and returned.
        Args:
            start: the field where the piece is moved from
            target: the field where the piece is moved to

        Returns:
            the piece that was removed from the end field
        """
        piece = self.pop(start)
        captured_piece = self.pop(target)
        self[target] = piece
        return captured_piece
