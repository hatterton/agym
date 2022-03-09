from dataclasses import dataclass

from .point import Vec2


T = float


@dataclass
class Line2:
    a: T
    b: T
    c: T

    def place(self, p: Vec2) -> T:
        return self.a * p.x + self.b * p.y + self.c
