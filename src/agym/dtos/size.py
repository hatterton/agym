from dataclasses import dataclass
from typing import Tuple


@dataclass
class Size:
    width: int
    height: int

    def to_tuple(self) -> Tuple[int, int]:
        return self.width, self.height
