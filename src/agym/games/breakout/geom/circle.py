from dataclasses import dataclass

from .point import Point


@dataclass
class Circle:
    center: Point
    radius: float
