from typing import Optional

from game.coordinate import Coordinate
from game.move import NormalMove
from game.move.board import Board
from game.move.move import Move
from game.piece.piece_type import PieceType


class PawnMove(NormalMove):
    def move(self, board: Board) -> None:
        super().move(board)

        en_passant_coordinate = self.en_passant_coordinate(board)
        if en_passant_coordinate is not None:
            board.pop(en_passant_coordinate)

        if self.is_double_move() and self.next_to_pawn(board):
            board.en_passant = self.new_en_passant(board)

        board.halfmove_clock = 0

    def en_passant_coordinate(self, board: Board) -> Optional[Coordinate]:
        if board.en_passant is None:
            return None

        if self.target_field != board.en_passant:
            return None

        if board.is_type(self.start_field.value, PieceType.WHITE):
            return Coordinate(board.en_passant.x, board.en_passant.y + 1)
        return Coordinate(board.en_passant.x, board.en_passant.y - 1)

    def next_to_pawn(self, board: Board) -> bool:
        if self.target_field.x != 0:
            left = Coordinate(self.target_field.x - 1, self.target_field.y)
            if board.is_type(left.value, PieceType.PAWN):
                return True
        if self.target_field.x != 7:
            right = Coordinate(self.target_field.x + 1, self.target_field.y)
            if board.is_type(right.value, PieceType.PAWN):
                return True
        return False

    def is_double_move(self) -> bool:
        return abs(self.start_field.y - self.target_field.y) == 2

    def new_en_passant(self, board: Board) -> Coordinate:
        if board.is_type(self.target_field.value, PieceType.WHITE):
            return Coordinate(self.start_field.x, self.start_field.y + 1)
        return Coordinate(self.start_field.x, self.start_field.y - 1)


class PawnPromotion(PawnMove):
    def __init__(self, start_field: Coordinate, target_field: Coordinate,
                 promote_to: PieceType):
        super().__init__(start_field, target_field)
        self.promote_to = promote_to

    def uci(self) -> str:
        return super().uci() + self.promote_to

    @classmethod
    def from_uci(cls, uci: str) -> "Move":
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        promotion = uci[4]
        return cls(start_field, target_field, PieceType.from_fen(promotion))

    def move(self, board: Board) -> None:
        super().move(board)
        piece = board[self.target_field]
        piece.type = self.promote_to
        board[self.target_field] = piece
