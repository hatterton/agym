from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T", int, float)


@dataclass
class Vec2(Generic[T]):
    x: T
    y: T

    def __neg__(self) -> "Vec2[T]":
        return Vec2(
            x=-self.x,
            y=-self.y,
        )

    def __add__(self, other: "Vec2[T]") -> "Vec2[T]":
        if isinstance(other, Vec2):
            return Vec2(
                x=self.x + other.x,
                y=self.y + other.y,
            )

        raise NotImplementedError

    def __sub__(self, other: "Vec2[T]") -> "Vec2[T]":
        return self + (-other)


Point = Vec2[float]
