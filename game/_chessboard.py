from game._board import _Board
from game.pieces import AbstractPiece, EmptyField, King, Queen, Bishop, Knight, Rook, Pawn


class _ChessBoard(_Board[AbstractPiece]):
    def __init__(self, board: list[AbstractPiece], white_to_move: bool,
                 castling_rights: str, en_passant: str, halfmove_clock: int,
                 fullmove_number: int):
        super().__init__(board)
        self.white_to_move = white_to_move
        self.castling_rights = castling_rights
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

    @classmethod
    def from_fen(cls, fen: str) -> '_ChessBoard':
        board = []
        fen = fen.split()

        position = fen[0].split("/")
        for row in position:
            for char in row:
                if char.isdigit():
                    board.extend([EmptyField.get_self()] * int(char))
                    continue

                white = not char.islower()
                char = char.lower()

                if char == "p":
                    board.append(Pawn(white))
                elif char == "r":
                    board.append(Rook(white))
                elif char == "n":
                    board.append(Knight(white))
                elif char == "b":
                    board.append(Bishop(white))
                elif char == "q":
                    board.append(Queen(white))
                elif char == "k":
                    board.append(King(white))
                else:
                    raise ValueError(f"Unknown piece {char}")

        board.reverse()

        white_to_move = fen[1] == "w"
        castling_rights = fen[2]
        en_passant = fen[3]
        halfmove_clock = int(fen[4])
        fullmove_number = int(fen[5])

        return cls(board, white_to_move, castling_rights, en_passant,
                   halfmove_clock, fullmove_number)

    def short_board(self) -> _Board[str]:
        return _Board[str]([piece.short for piece in self])

    def flat_short_board(self) -> tuple[str]:
        return tuple(piece.short for piece in self)

    def color_board(self) -> _Board[str | bool]:
        return _Board[str]([piece.is_white for piece in self])

    def material_difference(self) -> int:
        return sum(piece.value for piece in self)
