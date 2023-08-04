from typing import NamedTuple

index_to_letter = ord("h")


class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> "Coordinate":
        return Coordinate(self.x * other, self.y * other)

    def __rmul__(self, other: int) -> "Coordinate":
        return self * other

    @classmethod
    def from_uci(cls, uci: str) -> "Coordinate":
        """
        Parses a UCI string into a Coordinate.

        Args:
            uci: A string representing the UCI notation for a chess coordinate.

        Returns:
            Coordinate: A Coordinate representing the chess coordinate.

        Raises:
            ValueError: If the length of the UCI string is not 2.
        """
        if len(uci) != 2:
            raise ValueError(f"UCI must be 2 characters long, not {len(uci)}")
        x = index_to_letter - ord(uci[0])
        y = int(uci[1]) - 1
        return Coordinate(x, y)

    def uci(self):
        x = chr(index_to_letter - self.x)
        y = self.y + 1
        return f"{x}{y}"
