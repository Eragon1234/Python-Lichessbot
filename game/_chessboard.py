from game._board import _Board
from game.pieces import Piece
from game.pieces.piece_type import PieceType


class _ChessBoard:
    def __init__(self, board: list[Piece], white_to_move: bool,
                 castling_rights: str, en_passant: str, halfmove_clock: int,
                 fullmove_number: int):
        self._board = _Board[Piece](board)
        self._short_board = _Board[str]([piece.short for piece in self])

        self.white_to_move = white_to_move
        self.castling_rights = castling_rights
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

    def __getitem__(self, key: tuple[int, int]) -> Piece:
        return self._board[key]

    def __setitem__(self, key: tuple[int, int], value: Piece):
        self._board[key] = value
        self._short_board[key] = value.short

    def __iter__(self):
        return iter(self._board)

    def __hash__(self):
        return hash(self._board)

    @classmethod
    def from_fen(cls, fen: str) -> '_ChessBoard':
        board = []
        fen = fen.split()

        position = fen[0].split("/")
        for row in position:
            for char in row:
                if char.isdigit():
                    n = int(char)
                    board.extend(Piece(PieceType.EMPTY, "e") for _ in range(n))
                    continue

                white = not char.islower()
                char = char.lower()

                board.append(Piece(PieceType(char), white))

        board.reverse()

        white_to_move = fen[1] == "w"
        castling_rights = fen[2]
        en_passant = fen[3]
        halfmove_clock = int(fen[4])
        fullmove_number = int(fen[5])

        return cls(board, white_to_move, castling_rights, en_passant,
                   halfmove_clock, fullmove_number)

    def short_board(self) -> _Board[str]:
        return self._short_board

    def flat_short_board(self) -> tuple[str]:
        return tuple(self._short_board)

    def color_board(self) -> _Board[str | bool]:
        return _Board[str]([piece.is_white for piece in self])

    def material_difference(self) -> int:
        return sum(piece.value for piece in self)
