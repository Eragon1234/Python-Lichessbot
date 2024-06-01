from game.coordinate import Coordinate
from game.piece.color import Color


def is_start_rank(pos: Coordinate, color: Color) -> bool:
    """
    Checks if a given position is the start rank for a pawn of the color.

    Args:
        pos: The position to check.
        color: The color of the pawn.
        Defaults to the color of the piece.

    Returns:
        bool: whether the position is the start rank for a pawn.
    """
    start_rank = 1 if color is Color.WHITE else 6
    return pos.y == start_rank
