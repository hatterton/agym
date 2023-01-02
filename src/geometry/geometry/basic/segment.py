from dataclasses import dataclass

from .line import Line2
from .point import Point


@dataclass
class Segment:
    begin: Point
    end: Point

    @property
    def line(self) -> Line2:
        a = -(self.begin.y - self.end.y)
        b = self.begin.x - self.end.x
        c = -a * self.begin.x - b * self.begin.y

        return Line2(a=a, b=b, c=c)
