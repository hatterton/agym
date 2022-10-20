from typing import List, Iterable
from dataclasses import dataclass
from itertools import combinations
from statistics import mean

from ..basic import (
    Point,
    Segment,
)
from .rectangle import Rectangle


@dataclass
class Triangle:
    points: List[Point]

    @property
    def segments(self) -> Iterable[Segment]:
        for p1, p2 in combinations(self.points, 2):
            yield Segment(begin=p1, end=p2)

    @property
    def center(self) -> Point:
        c = (self.points[0] + self.points[1] + self.points[2]) / 3

        return c

    @property
    def bounding_box(self) -> Rectangle:
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]

        left = min(xs)
        right = max(xs)
        top = min(ys)
        bottom = max(ys)

        return Rectangle(
            left=left,
            top=top,
            width=right-left,
            height=bottom-top,
        )
