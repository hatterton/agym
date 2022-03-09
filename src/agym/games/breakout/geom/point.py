from typing import TypeVar, Generic
from dataclasses import dataclass

T = float


@dataclass
class Vec2:
    x: T
    y: T

    def __neg__(self) -> "Vec2":
        return Vec2(
            x=-self.x,
            y=-self.y,
        )

    def __add__(self, other: "Vec2") -> "Vec2":
        if isinstance(other, Vec2):
            return Vec2(
                x=self.x + other.x,
                y=self.y + other.y,
            )

        raise NotImplementedError

    def __sub__(self, other: "Vec2") -> "Vec2":
        return self + (-other)

    def __mul__(self, other) -> "Vec2":
        return Vec2(
            x=self.x * other,
            y=self.y * other,
        )

    def __truediv__(self, other) -> "Vec2":
        return self * (1 / other)


Point = Vec2

