from dataclasses import dataclass
from typing import List

T = float


@dataclass
class Vec2:
    x: T
    y: T

    def norm(self) -> T:
        return (self.x * self.x + self.y * self.y) ** 0.5

    def norm2(self) -> T:
        return self.x * self.x + self.y * self.y

    def normal(self) -> "Vec2":
        return Vec2(x=-self.y, y=self.x)

    def scalar(self, other: "Vec2") -> T:
        return self.x * other.x + self.y * other.y

    def copy(self) -> "Vec2":
        return Vec2(
            x=self.x,
            y=self.y,
        )

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

    def __rmul__(self, other) -> "Vec2":
        return self * other

    def __truediv__(self, other) -> "Vec2":
        return self * (1 / other)

    def __getitem__(self, idx: int) -> T:
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        else:
            raise ValueError(f"Out of index: {idx}")

    def __setitem__(self, idx: int, value: T) -> None:
        if idx == 0:
            self.x = value
        elif idx == 1:
            self.y = value
        else:
            raise ValueError(f"Out of index: {idx}")

    @classmethod
    def from_list(cls, arr: List[T]) -> "Point":
        assert len(arr) == 2

        return cls(
            x=arr[0],
            y=arr[1],
        )


Point = Vec2
