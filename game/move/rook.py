from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.move import NormalMove
from game.move.board import Board
from game.piece.color import Color


class RookMove(NormalMove):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

        self.old_castling_rights = CastlingRights.NONE

    def uci(self) -> str:
        return super().uci()

    @classmethod
    def from_uci(cls, uci: str) -> "RookMove":
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        return cls(start_field, target_field)

    def move(self, board: Board):
        self.old_castling_rights = board.castling_rights

        self.update_castling_rights(board)

        super().move(board)

    def undo(self, board: Board):
        board.castling_rights = self.old_castling_rights

        super().undo(board)

    def update_castling_rights(self, board: Board):
        moving_piece = board[self.start_field]

        if self.start_field.x == 0:
            remove_rights = CastlingRights.KING
        elif self.start_field.x == 7:
            remove_rights = CastlingRights.QUEEN
        else:
            return

        if moving_piece.color is Color.WHITE:
            remove_rights = remove_rights & CastlingRights.WHITE
        else:
            remove_rights = remove_rights & CastlingRights.BLACK

        board.castling_rights &= ~remove_rights
