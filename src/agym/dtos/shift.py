from dataclasses import dataclass
from typing import Tuple


@dataclass
class Shift:
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y
