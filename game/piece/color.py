from enum import Flag, auto


class Color(Flag):
    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()

    def enemy(self) -> "Color":
        if self is Color.EMPTY:
            return Color.EMPTY
        return Color.WHITE if self is Color.BLACK else Color.BLACK
