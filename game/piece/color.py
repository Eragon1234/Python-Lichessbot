from enum import Flag, auto
from functools import cache


class Color(Flag):
    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()

    @cache
    def enemy(self) -> "Color":
        if self is Color.EMPTY:
            return Color.EMPTY
        return Color.WHITE if self is Color.BLACK else Color.BLACK
