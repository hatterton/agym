from dataclasses import dataclass

from .point import Point

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

    # def __str__(self):
    #     result = "(({}, {}), ({}, {}))".format(
    #         self._w, self._h, *self.center)
    #     return result
