from typing import List
from agym.games.breakout.geom import Vec2


def almost_equal_float(a: float, b: float, eps: float = 1e-3) -> bool:
    return abs(a - b) < eps


Vec = Vec2
def almost_equal_vec(a: Vec, b: Vec) -> bool:
    return (
        almost_equal_float(a[0], b[0]) and
        almost_equal_float(a[1], b[1])
    )

almost_equal_point = almost_equal_vec
