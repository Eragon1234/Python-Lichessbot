from game.coordinate import Coordinate
from game.pieces.piece_type import PieceType

FORWARD = Coordinate(0, 1)
BACKWARD = Coordinate(0, -1)
LEFT = Coordinate(-1, 0)
RIGHT = Coordinate(1, 0)

POSSIBLE_MOVE_GROUPS = {
    PieceType.PAWN: [],
    PieceType.BISHOP: [
        [(RIGHT + FORWARD) * i for i in range(1, 8)],
        [(LEFT + FORWARD) * i for i in range(1, 8)],
        [(RIGHT + BACKWARD) * i for i in range(1, 8)],
        [(LEFT + BACKWARD) * i for i in range(1, 8)]
    ],
    PieceType.KNIGHT: [
        [Coordinate(i, j)] for i in [-2, -1, 1, 2] for j in [-2, -1, 1, 2] if abs(i) != abs(j)
    ],
    PieceType.ROOK: [
        [FORWARD * i for i in range(1, 8)],
        [BACKWARD * i for i in range(1, 8)],
        [RIGHT * i for i in range(1, 8)],
        [LEFT * i for i in range(1, 8)],
    ],
    PieceType.KING: [
        [Coordinate(i, j)] for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0
    ],
    PieceType.EMPTY: []
}

POSSIBLE_MOVE_GROUPS[PieceType.QUEEN] = POSSIBLE_MOVE_GROUPS[PieceType.BISHOP] + POSSIBLE_MOVE_GROUPS[PieceType.ROOK]
