from typing import Optional

from game.coordinate import Coordinate
from game.move import NormalMove
from game.move.board import Board, Piece
from game.move.move import Move
from game.piece.color import Color
from game.piece.piece_type import PieceType


class PawnMove(NormalMove):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

        self.en_passant_capture = None

    def move(self, board: Board) -> None:
        super().move(board)

        en_passant_coordinate = self.en_passant_coordinate(board)
        if en_passant_coordinate is not None:
            self.en_passant_capture = board.pop(en_passant_coordinate)

        if self.is_double_move() and self.next_to_pawn(board):
            board.en_passant = self.new_en_passant(board[self.target_field])

        board.halfmove_clock = 0

    def undo(self, board: Board) -> None:
        super().undo(board)

        if self.en_passant_capture is not None:
            board[self.en_passant_coordinate(board)] = self.en_passant_capture

    def en_passant_coordinate(self, board: Board) -> Optional[Coordinate]:
        moving_piece = board[self.start_field]
        if board.en_passant is None:
            return None

        if self.target_field != board.en_passant:
            return None

        if moving_piece.color == Color.WHITE:
            return Coordinate(board.en_passant.x, board.en_passant.y + 1)
        return Coordinate(board.en_passant.x, board.en_passant.y - 1)

    def next_to_pawn(self, board: Board) -> bool:
        if self.target_field.x != 0:
            left = Coordinate(self.target_field.x - 1, self.target_field.y)
            if board[left].type == PieceType.PAWN:
                return True
        if self.target_field.x != 7:
            right = Coordinate(self.target_field.x + 1, self.target_field.y)
            if board[right].type == PieceType.PAWN:
                return True
        return False

    def is_double_move(self) -> bool:
        return abs(self.start_field.y - self.target_field.y) == 2

    def new_en_passant(self, moving_piece: Piece) -> Coordinate:
        if moving_piece.color == Color.WHITE:
            return Coordinate(self.start_field.x, self.start_field.y + 1)
        return Coordinate(self.start_field.x, self.start_field.y - 1)


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

    def move(self, board: Board) -> None:
        super().move(board)
        piece = board[self.target_field]
        piece.type = self.promote_to
        board[self.target_field] = piece

    def undo(self, board: Board) -> None:
        piece = board[self.target_field]
        piece.type = PieceType.PAWN
        board[self.target_field] = piece
        super().undo(board)
