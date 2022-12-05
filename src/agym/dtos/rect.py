from dataclasses import dataclass

from .shift import Shift
from .size import Size


@dataclass
class Rect:
    shift: Shift
    size: Size

    def __init__(self, left: int, top: int, width: int, height: int) -> None:
        self.shift = Shift(x=left, y=top)
        self.size = Size(width=width, height=height)

    @classmethod
    def from_shift_size(cls, shift: Shift, size: Size) -> "Rect":
        return cls(
            left=shift.x,
            top=shift.y,
            width=size.width,
            height=size.height,
        )

    @classmethod
    def from_sides(cls, left: int, top: int, right: int, bottom: int) -> "Rect":
        return cls(
            left=left,
            top=top,
            width=right - left,
            height=bottom - top,
        )

    def copy(self) -> "Rect":
        return Rect(
            left=self.left,
            top=self.top,
            width=self.width,
            height=self.height,
        )

    # sides
    @property
    def left(self) -> int:
        return self.shift.x

    @left.setter
    def left(self, value: int) -> None:
        self.shift.x = value

    @property
    def top(self) -> int:
        return self.shift.y

    @top.setter
    def top(self, value: int) -> None:
        self.shift.y = value

    @property
    def right(self) -> int:
        return self.left + self.width

    @right.setter
    def right(self, value: int) -> None:
        self.left = value - self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    @bottom.setter
    def bottom(self, value: int) -> None:
        self.top = value - self.height

    # sizes
    @property
    def width(self) -> int:
        return self.width

    @width.setter
    def width(self, value: int) -> None:
        self.width = value

    @property
    def height(self) -> int:
        return self.height

    @height.setter
    def height(self, value: int) -> None:
        self.height = value

    # center
    @property
    def center(self) -> Shift:
        return Shift(x=self.centerx, y=self.centery)

    @center.setter
    def center(self, value: Shift) -> None:
        self.centerx = value.x
        self.centery = value.y

    @property
    def centerx(self) -> int:
        return self.left + self.width // 2

    @centerx.setter
    def centerx(self, value: int) -> None:
        self.left = value - self.width // 2

    @property
    def centery(self) -> int:
        return self.top + self.height // 2

    @centery.setter
    def centery(self, value: int) -> None:
        self.top = value - self.height // 2

    def __repr__(self) -> str:
        return f"(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"
