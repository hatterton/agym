from typing import List, Iterable
from dataclasses import dataclass
from itertools import combinations
from statistics import mean

from .point import Point
from .segment import Segment

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
