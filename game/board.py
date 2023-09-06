from collections.abc import Iterator
from typing import Optional

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.move.factory import move_factory
from game.piece.color import Color
from game.piece.piece import Piece
from game.piece.piece_type import PieceType


class Board:
    def __init__(self, board: list[Piece], turn: Color,
                 castling_rights: CastlingRights,
                 en_passant: Optional[Coordinate],
                 halfmove_clock: int, fullmove_number: int):
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

    def iter_pieces(self) -> Iterator[tuple[Coordinate, Piece]]:
        """
        Iterate over the pieces of the board.
        """
        for i, piece in enumerate(self):
            yield Coordinate.from_index(i), piece

    def __hash__(self) -> int:
        return hash(tuple(self._board))

    @classmethod
    def from_fen(cls, fen: str) -> 'Board':
        board = []
        fen_parts = fen.split()

        position = fen_parts[0].split("/")
        for row in position:
            for char in row:
                if char.isdigit():
                    n = int(char)
                    board.extend(Piece(move_factory,
                                       PieceType.EMPTY,
                                       Color.EMPTY) for _ in range(n))
                    continue

                board.append(Piece.from_fen(char, move_factory))

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

    def color_at(self, position: tuple[int, int]) -> Color:
        return self[position].color

    def pop(self, position: tuple[int, int]) -> Piece:
        piece = self[position]
        self[position] = Piece(move_factory, PieceType.EMPTY, Color.EMPTY)
        return piece

    def do_move(self, start: Coordinate, target: Coordinate) -> Piece:
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

