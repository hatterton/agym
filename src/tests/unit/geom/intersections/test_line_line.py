import pytest

from agym.games.breakout.geom import (
    Line2,
    Circle,
    Point,
    get_intersection_line_line,
)

from tests.math_utils import (
    almost_equal_point,
    almost_equal_float,
)


@pytest.mark.geom
@pytest.mark.intersections
@pytest.mark.line
class TestIntersectionsLineLine:
    def test_line_line_intersection(self):
        l1 = Line2(a=1, b=0, c=0)
        l2 = Line2(a=0, b=1, c=0)
        ip = get_intersection_line_line(l1, l2)
        ep = Point(x=0, y=0)
        assert ip is not None
        assert almost_equal_point(ip, ep)

        l1 = Line2(a=1, b=2, c=0)
        l2 = Line2(a=1, b=2, c=1)
        ip = get_intersection_line_line(l1, l2)
        assert ip is None

        l1 = Line2(a=0.5, b=-1, c=2)
        l2 = Line2(a=2, b=-1, c=-4)
        ip = get_intersection_line_line(l1, l2)
        ep = Point(x=4, y=4)
        assert ip is not None
        assert almost_equal_point(ip, ep)

        l1 = Line2(a=1, b=2, c=0)
        l2 = Line2(a=1, b=2, c=0)
        ip = get_intersection_line_line(l1, l2)
        assert ip is None

