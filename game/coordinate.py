from typing import NamedTuple

index_to_letter = ord("h")


class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)
    
    @classmethod
    def from_uci(cls, uci: str):
        x = index_to_letter - ord(uci[0])
        y = int(uci[1]) - 1
        return x, y

    def uci(self):
        x = chr(index_to_letter - self.x)
        y = self.y + 1
        return f"{x}{y}"
