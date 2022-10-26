from dataclasses import dataclass

from ..basic import Point


@dataclass
class Rectangle:
    left: float
    top: float
    width: float
    height: float

    @classmethod
    def from_rect(cls, rect: "Rectangle") -> "Rectangle":
        return cls(
            left=rect.left,
            top=rect.top,
            width=rect.width,
            height=rect.height,
        )

    def copy(self) -> "Rectangle":
        return Rectangle(
            left=self.left,
            top=self.top,
            width=self.width,
            height=self.height,
        )

    @property
    def bottom(self) -> float:
        return self.top + self.height

    @bottom.setter
    def bottom(self, value: float) -> None:
        self.top = value - self.height

    @property
    def right(self) -> float:
        return self.left + self.width

    @right.setter
    def right(self, value: float) -> None:
        self.left = value - self.width

    @property
    def w(self) -> float:
        return self.width

    @w.setter
    def w(self, value: float) -> None:
        self.width = value

    @property
    def h(self) -> float:
        return self.height

    @h.setter
    def h(self, value: float) -> None:
        self.height = value

    @property
    def center(self) -> Point:
        return Point(x=self.centerx, y=self.centery)

    @center.setter
    def center(self, value: Point) -> None:
        self.centerx = value.x
        self.centery = value.y

    @property
    def centerx(self) -> float:
        return self.left + self.width / 2

    @centerx.setter
    def centerx(self, value: float) -> None:
        self.left = value - self.width / 2

    @property
    def centery(self) -> float:
        return self.top + self.height / 2

    @centery.setter
    def centery(self, value: float) -> None:
        self.top = value - self.height / 2

    def union(self, rect: "Rectangle") -> "Rectangle":
        left = min(self.left, rect.left)
        right = max(self.right, rect.right)
        top = min(self.top, rect.top)
        bottom = max(self.bottom, rect.bottom)
        return Rectangle(
            left=left,
            top=top,
            width=right-left,
            height=bottom-top,
        )

    def is_intersected(self, rect: "Rectangle") -> bool:
        if self.left > rect.right or rect.left > self.right:
            return False

        elif self.top > rect.bottom or rect.top > self.bottom:
            return False

        return True

    def contains(self, p: Point) -> bool:
        if p.x < self.left or p.x > self.right:
            return False

        elif p.y < self.top or p.y > self.bottom:
            return False

        return True

    @property
    def bounding_box(self) -> "Rectangle":
        return self

    def __repr__(self) -> str:
        return f"(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"
