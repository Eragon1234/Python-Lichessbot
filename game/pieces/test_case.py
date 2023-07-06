from game.types import Position, Positions


class Case:
    def __init__(self, position: Position, expected: Positions):
        self.position = position
        self.expected = expected
        from game._chessboard import _ChessBoard
        self.board = _ChessBoard.from_fen("8/8/8/8/8/8/8/8 w - - 0 1").color_board()

    def with_piece(self, color: bool | str, x: int, y: int):
        self.board[x, y] = color
        return self
