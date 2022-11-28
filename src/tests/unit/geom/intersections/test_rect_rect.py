import pytest

from agym.games.breakout.geom import Point, Rectangle, is_intersected
from tests.math_utils import almost_equal_float, almost_equal_point


@pytest.mark.geom
@pytest.mark.intersections
@pytest.mark.rectangle
class TestIntersectionsRectangleRectangle:
    def test_rectangle_rectangle_intersection(self):
        r1 = Rectangle(
            left=-5,
            top=-5,
            width=10,
            height=10,
        )

        r2 = Rectangle(
            left=-5,
            top=-5,
            width=10,
            height=10,
        )
        assert is_intersected(r1, r2)
        assert is_intersected(r2, r1)

        r2 = Rectangle(
            left=-2,
            top=-2,
            width=4,
            height=4,
        )
        assert is_intersected(r1, r2)
        assert is_intersected(r2, r1)

        r2 = Rectangle(
            left=-10,
            top=-10,
            width=20,
            height=20,
        )
        assert is_intersected(r1, r2)
        assert is_intersected(r2, r1)

        r2 = Rectangle(
            left=5,
            top=0,
            width=10,
            height=10,
        )
        assert not is_intersected(r1, r2)
        assert not is_intersected(r2, r1)

        r2 = Rectangle(
            left=5,
            top=5,
            width=10,
            height=10,
        )
        assert not is_intersected(r1, r2)
        assert not is_intersected(r2, r1)

        r2 = Rectangle(
            left=10,
            top=10,
            width=10,
            height=10,
        )
        assert not is_intersected(r1, r2)
        assert not is_intersected(r2, r1)
