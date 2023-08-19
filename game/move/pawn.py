from typing import Optional

from game.coordinate import Coordinate
from game.move._chessboard import _ChessBoard
from game.move.move import Move
from game.piece.color import Color
from game.piece.piece_type import PieceType


class PawnMove(Move):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

        self.old_en_passant = None
        self.en_passant_capture = None

    def uci(self) -> str:
        return super().uci()

    @classmethod
    def from_uci(cls, uci: str) -> "Move":
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        return cls(start_field, target_field)

    def move(self, board: _ChessBoard) -> None:
        self.old_en_passant = board.en_passant

        en_passant_coordinate = self.en_passant_coordinate(board)
        if en_passant_coordinate is not None:
            self.en_passant_capture = board.pop(en_passant_coordinate)

        board.en_passant = "-"

        if self.is_double_move():
            board.en_passant = self.new_en_passant(board)

        super().move(board)

        board.turn = board.turn.enemy()

    def undo(self, board: _ChessBoard) -> None:
        board.en_passant = self.old_en_passant

        super().undo(board)

        board.turn = board.turn.enemy()

        if self.en_passant_capture is not None:
            board[self.en_passant_coordinate(board)] = self.en_passant_capture

    def en_passant_coordinate(self, board: _ChessBoard) -> Optional[Coordinate]:
        moving_piece = board[self.start_field]
        if board.en_passant == "-":
            return None

        coordinate = Coordinate.from_uci(board.en_passant)
        if self.target_field != coordinate:
            return None

        if moving_piece.color == Color.WHITE:
            return Coordinate(coordinate.x, coordinate.y + 1)
        else:
            return Coordinate(coordinate.x, coordinate.y - 1)

    def is_double_move(self) -> bool:
        return abs(self.start_field.y - self.target_field.y) == 2

    def new_en_passant(self, board: _ChessBoard) -> str:
        moving_piece = board[self.start_field]
        if moving_piece.color == Color.WHITE:
            return Coordinate(self.start_field.x, self.start_field.y + 1).uci()
        else:
            return Coordinate(self.start_field.x, self.start_field.y - 1).uci()


class PawnPromotion(PawnMove):
    def __init__(self, start_field: Coordinate, target_field: Coordinate,
                 promote_to: PieceType):
        super().__init__(start_field, target_field)
        self.promote_to = promote_to

    def uci(self) -> str:
        return super().uci() + self.promote_to.value

    @classmethod
    def from_uci(cls, uci: str) -> "Move":
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        promotion = uci[4]
        return cls(start_field, target_field, PieceType(promotion))

    def move(self, board: _ChessBoard) -> None:
        super().move(board)
        board[self.target_field].type = self.promote_to

    def undo(self, board: _ChessBoard) -> None:
        board[self.target_field].type = PieceType.PAWN
        super().undo(board)
