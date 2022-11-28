import pytest

from agym.games.breakout.geom import Circle, Point, Triangle, is_intersected
from tests.math_utils import almost_equal_float, almost_equal_point


@pytest.mark.geom
@pytest.mark.intersections
@pytest.mark.circle
@pytest.mark.triangle
class TestIntersectionsCircleTriangle:
    def test_triangle_circle_intersection(self):
        t = Triangle(
            points=[
                Point(x=10, y=0),
                Point(x=-10, y=0),
                Point(x=0, y=10),
            ]
        )

        c = Circle(
            center=Point(x=0, y=1),
            radius=1,
        )
        assert is_intersected(t, c)
        assert is_intersected(c, t)

        c = Circle(
            center=Point(x=0, y=-1),
            radius=2,
        )
        assert is_intersected(t, c)
        assert is_intersected(c, t)

        c = Circle(
            center=Point(x=0, y=-1),
            radius=1,
        )
        assert not is_intersected(t, c)
        assert not is_intersected(c, t)

        c = Circle(
            center=Point(x=20, y=-1),
            radius=2,
        )
        assert not is_intersected(t, c)
        assert not is_intersected(c, t)

        c = Circle(
            center=Point(x=11, y=-1),
            radius=2,
        )
        assert is_intersected(t, c)
        assert is_intersected(c, t)
