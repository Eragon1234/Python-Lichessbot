from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.move import NormalMove
from game.move.board import Board
from game.piece.color import Color


class RookMove(NormalMove):
    def uci(self) -> str:
        return super().uci()

    @classmethod
    def from_uci(cls, uci: str) -> "RookMove":
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        return cls(start_field, target_field)

    def move(self, board: Board):
        self.update_castling_rights(board)

        super().move(board)

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
