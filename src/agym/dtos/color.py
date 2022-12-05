from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Color:
    red: int
    green: int
    blue: int
    alpha: int = 255

    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.red, self.green, self.blue, self.alpha)
