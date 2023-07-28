from game.coordinate import Coordinate
from game.pieces.piece_type import PieceType

POSSIBLE_MOVE_GROUPS = {
    PieceType.PAWN: [],
    PieceType.BISHOP: [
        [Coordinate(i, i) for i in range(1, 8)],
        [Coordinate(i, -i) for i in range(1, 8)],
        [Coordinate(-i, i) for i in range(1, 8)],
        [Coordinate(-i, -i) for i in range(1, 8)]
    ],
    PieceType.KNIGHT: [
        [Coordinate(i, j)] for i in [-2, -1, 1, 2] for j in [-2, -1, 1, 2] if abs(i) != abs(j)
    ],
    PieceType.ROOK: [
        [Coordinate(i, 0) for i in range(1, 8)],
        [Coordinate(-i, 0) for i in range(1, 8)],
        [Coordinate(0, i) for i in range(1, 8)],
        [Coordinate(0, -i) for i in range(1, 8)],
    ],
    PieceType.KING: [
        [Coordinate(i, j)] for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0
    ],
    PieceType.EMPTY: []
}

POSSIBLE_MOVE_GROUPS[PieceType.QUEEN] = POSSIBLE_MOVE_GROUPS[PieceType.BISHOP] + POSSIBLE_MOVE_GROUPS[PieceType.ROOK]
