from game.pieces.piece_type import PieceType

POSSIBLE_MOVE_GROUPS = {
    PieceType.PAWN: [],
    PieceType.BISHOP: [
        [(i, i) for i in range(1, 8)],
        [(i, -i) for i in range(1, 8)],
        [(-i, i) for i in range(1, 8)],
        [(-i, -i) for i in range(1, 8)]
    ],
    PieceType.KNIGHT: [
        [(i, j)] for i in [-2, -1, 1, 2] for j in [-2, -1, 1, 2] if abs(i) != abs(j)
    ],
    PieceType.ROOK: [
        [(i, 0) for i in range(1, 8)],
        [(-i, 0) for i in range(1, 8)],
        [(0, i) for i in range(1, 8)],
        [(0, -i) for i in range(1, 8)],
    ],
    PieceType.KING: [
        [(i, j)] for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0
    ],
    PieceType.EMPTY: []
}

POSSIBLE_MOVE_GROUPS[PieceType.QUEEN] = POSSIBLE_MOVE_GROUPS[PieceType.BISHOP] + POSSIBLE_MOVE_GROUPS[PieceType.ROOK]
