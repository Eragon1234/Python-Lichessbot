from enum import Enum


class Color(Enum):
    WHITE = True
    BLACK = False
    EMPTY = "EmptyField"

    def enemy_color(self) -> "Color":
        if self == Color.EMPTY:
            return Color.EMPTY
        return Color.WHITE if self == Color.BLACK else Color.BLACK
