import pytest

from agym.games.breakout.geom import Point, Triangle, is_intersected
from tests.math_utils import almost_equal_float, almost_equal_point


@pytest.mark.geom
@pytest.mark.intersections
@pytest.mark.triangle
class TestIntersectionsTriangleTriangle:
    def test_triangle_triangle_intersection(self):
        t1 = Triangle(
            points=[
                Point(x=10, y=0),
                Point(x=-10, y=0),
                Point(x=0, y=10),
            ]
        )

        t2 = Triangle(
            points=[
                Point(x=-5, y=10),
                Point(x=5, y=10),
                Point(x=0, y=11),
            ]
        )
        assert not is_intersected(t1, t2)
        assert not is_intersected(t2, t1)

        t2 = Triangle(
            points=[
                Point(x=-5, y=10),
                Point(x=5, y=10),
                Point(x=0, y=9),
            ]
        )
        assert is_intersected(t1, t2)
        assert is_intersected(t2, t1)

        t2 = Triangle(
            points=[
                Point(x=1, y=1),
                Point(x=-1, y=1),
                Point(x=0, y=2),
            ]
        )
        assert is_intersected(t1, t2)
        assert is_intersected(t2, t1)

        t2 = Triangle(
            points=[
                Point(x=20, y=-1),
                Point(x=-20, y=-1),
                Point(x=0, y=1),
            ]
        )
        assert is_intersected(t1, t2)
        assert is_intersected(t2, t1)

        t2 = Triangle(
            points=[
                Point(x=10, y=0),
                Point(x=-10, y=0),
                Point(x=0, y=10),
            ]
        )
        assert is_intersected(t1, t2)
        assert is_intersected(t2, t1)

        t2 = Triangle(
            points=[
                Point(x=-12, y=2),
                Point(x=-12, y=1),
                Point(x=12, y=2),
            ]
        )
        assert is_intersected(t1, t2)
        assert is_intersected(t2, t1)

        t2 = Triangle(
            points=[
                Point(x=20, y=10),
                Point(x=-20, y=10),
                Point(x=0, y=-10),
            ]
        )
        assert is_intersected(t1, t2)
        assert is_intersected(t2, t1)

        t2 = Triangle(
            points=[
                Point(x=10, y=0),
                Point(x=-10, y=0),
                Point(x=0, y=0),
            ]
        )
        assert not is_intersected(t1, t2)
        assert not is_intersected(t2, t1)

        t2 = Triangle(
            points=[
                Point(x=10, y=0),
                Point(x=-10, y=0),
                Point(x=0, y=-1),
            ]
        )
        assert not is_intersected(t1, t2)
        assert not is_intersected(t2, t1)
