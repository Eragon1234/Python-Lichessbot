from game.coordinate import Coordinate
from game.piece.piece_type import PieceType

FORWARD = Coordinate(0, 1)
BACKWARD = Coordinate(0, -1)
LEFT = Coordinate(-1, 0)
RIGHT = Coordinate(1, 0)
NO_MOVE = Coordinate(0, 0)

MOVE_GROUPS = {
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
        [i + j]
        for i in (LEFT, NO_MOVE, RIGHT)
        for j in (FORWARD, NO_MOVE, BACKWARD)
        if i != NO_MOVE or j != NO_MOVE
    ],
    PieceType.EMPTY: []
}

MOVE_GROUPS[PieceType.QUEEN] = (MOVE_GROUPS[PieceType.BISHOP]
                                + MOVE_GROUPS[PieceType.ROOK])
