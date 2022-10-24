import pytest

from agym.games.breakout.geom import (
    Circle,
    Point,
    Segment,
    get_intersection_circle_segment,
)

from tests.math_utils import (
    almost_equal_point,
    almost_equal_float,
)


@pytest.mark.geom
@pytest.mark.intersections
@pytest.mark.circle
@pytest.mark.segment
class TestIntersectionsCircleSegment:
    def test_circle_segment_intersection(self):
        s = Segment(
            begin=Point(x=0, y=0),
            end=Point(x=5, y=5),
        )

        c = Circle(
            center=Point(x=0, y=5),
            radius=1,
        )
        ip = get_intersection_circle_segment(c, s)
        assert ip is None

        c = Circle(
            center=Point(x=-1, y=-1),
            radius=1,
        )
        ip = get_intersection_circle_segment(c, s)
        assert ip is None

        c = Circle(
            center=Point(x=6, y=6),
            radius=2,
        )
        ip = get_intersection_circle_segment(c, s)
        ep = Point(x=5, y=5)
        assert ip is not None
        assert almost_equal_point(ip, ep)

        c = Circle(
            center=Point(x=0, y=5),
            radius=5,
        )
        ip = get_intersection_circle_segment(c, s)
        ep = Point(x=2.5, y=2.5)
        assert ip is not None
        assert almost_equal_point(ip, ep)


    def test_circle_vertical_segment_intersection(self):
        s = Segment(
            begin=Point(x=0, y=0),
            end=Point(x=0, y=5),
        )

        c = Circle(
            center=Point(x=4, y=-4),
            radius=5,
        )
        ip = get_intersection_circle_segment(c, s)
        assert ip is None

        c = Circle(
            center=Point(x=4, y=-2),
            radius=5,
        )
        ip = get_intersection_circle_segment(c, s)
        ep = Point(x=0, y=0)
        assert almost_equal_point(ip, ep)


    def test_circle_horisontal_segment_intersection(self):
        s = Segment(
            begin=Point(x=0, y=0),
            end=Point(x=5, y=0),
        )

        c = Circle(
            center=Point(x=-4, y=4),
            radius=5,
        )
        ip = get_intersection_circle_segment(c, s)
        assert ip is None

        c = Circle(
            center=Point(x=-4, y=2),
            radius=5,
        )
        ip = get_intersection_circle_segment(c, s)
        ep = Point(x=0, y=0)
        assert almost_equal_point(ip, ep)
