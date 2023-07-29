from game._board import _Board
from game.pieces import Piece, Color, PieceType


class _ChessBoard:
    def __init__(self, board: list[Piece], white_to_move: bool,
                 castling_rights: str, en_passant: str, halfmove_clock: int,
                 fullmove_number: int):
        self._board = _Board[Piece](board)

        self.white_to_move = white_to_move
        self.castling_rights = castling_rights
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

    def __getitem__(self, key: tuple[int, int]) -> Piece:
        return self._board[key]

    def __setitem__(self, key: tuple[int, int], value: Piece):
        self._board[key] = value

    def __iter__(self):
        return iter(self._board)

    def __hash__(self):
        return hash(self._board)

    @classmethod
    def from_fen(cls, fen: str) -> '_ChessBoard':
        board = []
        fen_parts = fen.split()

        position = fen_parts[0].split("/")
        for row in position:
            for char in row:
                if char.isdigit():
                    n = int(char)
                    board.extend(Piece(PieceType.EMPTY, Color.EMPTY) for _ in range(n))
                    continue

                board.append(Piece.from_fen(char))

        board.reverse()

        white_to_move = fen_parts[1] == "w"
        castling_rights = fen_parts[2]
        en_passant = fen_parts[3]
        halfmove_clock = int(fen_parts[4])
        fullmove_number = int(fen_parts[5])

        return cls(board, white_to_move, castling_rights, en_passant,
                   halfmove_clock, fullmove_number)

    def material_difference(self) -> int:
        return sum(piece.value for piece in self)

    def color_at(self, position: tuple[int, int]) -> Color:
        return self._board[position].color
