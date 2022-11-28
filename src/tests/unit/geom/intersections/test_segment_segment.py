import pytest

from agym.games.breakout.geom import (
    Point,
    Segment,
    get_intersection_segment_segment,
)
from tests.math_utils import almost_equal_float, almost_equal_point


@pytest.mark.geom
@pytest.mark.intersections
@pytest.mark.segment
class TestIntersectionsSegmentSegment:
    def test_segment_segment_intersection(self):
        seg1 = Segment(
            begin=Point(x=-5, y=0),
            end=Point(x=5, y=0),
        )
        seg2 = Segment(
            begin=Point(x=0, y=5),
            end=Point(x=0, y=-5),
        )
        ip = get_intersection_segment_segment(seg1, seg2)
        ep = Point(x=0, y=0)
        assert ip is not None
        assert almost_equal_point(ip, ep)

        seg1 = Segment(
            begin=Point(x=1, y=0),
            end=Point(x=5, y=0),
        )
        seg2 = Segment(
            begin=Point(x=0, y=-5),
            end=Point(x=0, y=5),
        )
        assert get_intersection_segment_segment(seg1, seg2) is None
        assert get_intersection_segment_segment(seg2, seg1) is None

        seg1 = Segment(
            begin=Point(x=0, y=0),
            end=Point(x=0, y=5),
        )
        seg2 = Segment(
            begin=Point(x=-5, y=0),
            end=Point(x=5, y=0),
        )
        assert get_intersection_segment_segment(seg1, seg2) is None
        assert get_intersection_segment_segment(seg2, seg1) is None

        seg1 = Segment(
            begin=Point(x=0, y=5),
            end=Point(x=0, y=-5),
        )
        seg2 = Segment(
            begin=Point(x=0, y=1),
            end=Point(x=0, y=-1),
        )
        assert get_intersection_segment_segment(seg1, seg2) is None
        assert get_intersection_segment_segment(seg2, seg1) is None
