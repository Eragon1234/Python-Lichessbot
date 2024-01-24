from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.move.board import Board
from game.move.move import PureMove
from game.move.normal import NormalMove
from game.piece.piece_type import PieceType


class KingMove(NormalMove):
    def move(self, board: Board) -> None:
        super().move(board)

        self.update_castling_rights(board)

    def update_castling_rights(self, board: Board) -> None:
        if board.is_type(self.target_field.value, PieceType.WHITE):
            remove_rights = CastlingRights.WHITE
        else:
            remove_rights = CastlingRights.BLACK

        board.castling_rights &= ~remove_rights


class CastleMove(KingMove):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

    def move(self, board: Board) -> None:
        super().move(board)

        self.get_rook_move().move(board)

    def get_rook_move(self) -> PureMove:
        if self.target_field.x == 1:
            rook_start = Coordinate(0, self.target_field.y)
            rook_target = Coordinate(2, self.target_field.y)
        else:
            rook_start = Coordinate(7, self.target_field.y)
            rook_target = Coordinate(4, self.target_field.y)

        return PureMove(rook_start, rook_target)
