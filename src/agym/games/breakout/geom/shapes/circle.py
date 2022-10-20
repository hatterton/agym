from dataclasses import dataclass

from ..basic import Point
from .rectangle import Rectangle


@dataclass
class Circle:
    center: Point
    radius: float

    @property
    def bounding_box(self) -> Rectangle:
        return Rectangle(
            left=self.center.x-self.radius,
            top=self.center.y-self.radius,
            width=2*self.radius,
            height=2*self.radius,
        )
