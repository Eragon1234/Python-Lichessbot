import copy
from collections.abc import Iterator
from typing import Optional

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.piece.color import Color
from game.piece.piece_type import PieceType

coordinates = [Coordinate.from_index(i) for i in range(64)]

masks = [1 << i for i in range(64)]


class Board:
    def __init__(self, value: int, _boards: dict[PieceType, int], turn: Color,
                 castling_rights: CastlingRights,
                 en_passant: Optional[Coordinate],
                 halfmove_clock: int, fullmove_number: int):
        self.value = value
        self._boards: dict[PieceType, int] = _boards
        self.turn = turn
        self.castling_rights = castling_rights
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

    def __hash__(self) -> int:
        return hash(self.fen())

    def __eq__(self, other: "Board") -> bool:
        return (self._boards == other._boards and
                self.turn == other.turn and
                self.castling_rights == other.castling_rights and
                self.en_passant == other.en_passant)

    def clone(self) -> 'Board':
        return copy.deepcopy(self)

    def is_type(self, i: int | Coordinate, t: PieceType):
        if isinstance(i, Coordinate):
            i = i.value
        return self._boards[t] & (masks[i])

    def __getitem__(self, item: Coordinate | int) -> PieceType:
        if isinstance(item, Coordinate):
            item = item.value
        if self._boards[PieceType.EMPTY] & masks[item]:
            return PieceType.EMPTY
        piece_type = PieceType(0)
        for t, b in self._boards.items():
            if not b & (masks[item]):
                continue
            piece_type |= t
        return piece_type

    def __setitem__(self, key: Coordinate | int, value: PieceType):
        if isinstance(key, Coordinate):
            key = key.value
        self.value -= self[key].value_at(key)
        self._clear_bits(key)
        for t in value:
            self._boards[t] |= masks[key]
        self.value += value.value_at(key)

    def _clear_bits(self, i: int) -> None:
        mask = ~(masks[i])
        for t in self._boards:
            self._boards[t] &= mask

    def __iter__(self) -> Iterator[PieceType]:
        return (self[i] for i in range(64))

    def iter_rows(self) -> Iterator[list[PieceType]]:
        """
        Iterate over the rows of the board.
        The rows are a8-h8, a7-h7, ..., a1-h1
        """
        for i in reversed(range(8)):
            yield [self[Coordinate(j, i)] for j in reversed(range(8))]

    @classmethod
    def from_list(cls, board: list[PieceType], turn: Color,
                  castling_rights: CastlingRights,
                  en_passant: Optional[Coordinate],
                  halfmove_clock: int, fullmove_number: int):
        new_board = cls(
            0,
            {t: 0 for t in PieceType},
            turn,
            castling_rights,
            en_passant,
            halfmove_clock,
            fullmove_number
        )

        for i, piece in enumerate(board):
            new_board[i] = piece

        new_board.value = new_board.material_difference()

        return new_board

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

        return cls.from_list(board, turn, castling_rights, en_passant,
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

    def approximate_board_state(self) -> int:
        state = 0
        for board in self._boards:
            state |= self._boards[board]
            state = state << 64
        return state

    def material_difference(self) -> int:
        value = 0
        for color in PieceType.COLORS:
            for piece_type in ~PieceType.COLORS:
                bitmask = self._boards[color] & self._boards[piece_type]
                count = bitmask.bit_count()
                piece_type = color | piece_type
                value += piece_type.piece_value * count
        return value

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
