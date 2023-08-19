from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.move._chessboard import _ChessBoard
from game.move.move import Move, PureMove
from game.piece.color import Color


class KingMove(Move):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

        self.old_en_passant = "-"
        self.old_castling_rights = None

    def uci(self) -> str:
        return f"{self.start_field.uci()}{self.target_field.uci()}"

    @classmethod
    def from_uci(cls, uci: str) -> "Move":
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        return cls(start_field, target_field)

    def move(self, board: _ChessBoard) -> None:
        self.old_en_passant = board.en_passant
        self.old_castling_rights = board.castling_rights

        self.update_castling_rights(board)

        super().move(board)

        board.turn = board.turn.enemy()

        board.en_passant = "-"

    def undo(self, board: _ChessBoard) -> None:
        board.en_passant = self.old_en_passant
        board.castling_rights = self.old_castling_rights

        super().undo(board)

        board.turn = board.turn.enemy()

    def update_castling_rights(self, board: _ChessBoard) -> None:
        moving_piece = board[self.start_field]
        if moving_piece.color is Color.WHITE:
            remove_rights = CastlingRights.WHITE
        else:
            remove_rights = CastlingRights.BLACK

        board.castling_rights &= ~remove_rights


class CastleMove(KingMove):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

        self.rook_move = None

    def move(self, board: _ChessBoard) -> None:
        super().move(board)

        self.rook_move = self.get_rook_move()
        self.rook_move.move(board)

    def undo(self, board: _ChessBoard) -> None:
        self.rook_move.undo(board)

        super().undo(board)

    def get_rook_move(self) -> PureMove:
        if self.target_field.x == 1:
            rook_start = Coordinate(0, self.target_field.y)
            rook_target = Coordinate(2, self.target_field.y)
        else:
            rook_start = Coordinate(7, self.target_field.y)
            rook_target = Coordinate(4, self.target_field.y)

        return PureMove(rook_start, rook_target)
