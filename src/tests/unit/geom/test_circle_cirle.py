import pytest

from agym.games.breakout.geom import (
    Circle,
    Point,
    is_intersected,
)


@pytest.mark.geom
@pytest.mark.intersections
@pytest.mark.circle
class TestIntersectionsCircleCircle:
    def test_circle_circle_intersection(self):
        c1 = Circle(
            center=Point(x=0, y=0),
            radius=10,
        )
        c2 = Circle(
            center=Point(x=0, y=0),
            radius=1,
        )
        assert is_intersected(c1, c2)

        c2 = Circle(
            center=Point(x=7, y=7),
            radius=1,
        )
        assert is_intersected(c1, c2)

        c2 = Circle(
            center=Point(x=9, y=9),
            radius=1,
        )
        assert not is_intersected(c1, c2)

        c2 = Circle(
            center=Point(x=10, y=0),
            radius=0,
        )
        assert not is_intersected(c1, c2)

        c2 = Circle(
            center=Point(x=11, y=0),
            radius=1,
        )
        assert not is_intersected(c1, c2)

