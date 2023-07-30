from enum import Flag, auto


class Color(Flag):
    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()

    def enemy_color(self) -> "Color":
        if self == Color.EMPTY:
            return Color.EMPTY
        return Color.WHITE if self == Color.BLACK else Color.BLACK
