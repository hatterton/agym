import pytest

from agym.games.breakout.geom import (
    Point,
    Vec2,
    Line2,
    Segment,
    Triangle,
    Circle,
    Rectangle,
    is_intersected,
    get_intersection_segment_segment,
    get_intersection_line_line,
)


def almost_equal_float(a: float, b: float, eps: float = 1e-4) -> bool:
    return abs(a - b) < eps


def almost_equal_point(a: Point, b: Point, eps: float = 1e-4) -> bool:
    return (
        almost_equal_float(a.x, b.x, eps) and
        almost_equal_float(a.y, b.y, eps)
    )


def test_line_line_intersection():
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


def test_segment_segment_intersection():
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


def test_circle_circle_intersection():
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


def test_triangle_triangle_intersection():
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

    t2 = Triangle(
        points=[
            Point(x=-5, y=10),
            Point(x=5, y=10),
            Point(x=0, y=9),
        ]
    )
    assert is_intersected(t1, t2)

    t2 = Triangle(
        points=[
            Point(x=1, y=1),
            Point(x=-1, y=1),
            Point(x=0, y=2),
        ]
    )
    assert is_intersected(t1, t2)

    t2 = Triangle(
        points=[
            Point(x=20, y=-1),
            Point(x=-20, y=-1),
            Point(x=0, y=1),
        ]
    )
    assert is_intersected(t1, t2)

    t2 = Triangle(
        points=[
            Point(x=10, y=0),
            Point(x=-10, y=0),
            Point(x=0, y=10),
        ]
    )
    assert is_intersected(t1, t2)

    t2 = Triangle(
        points=[
            Point(x=-12, y=2),
            Point(x=-12, y=1),
            Point(x=12, y=2),
        ]
    )
    assert is_intersected(t1, t2)

    t2 = Triangle(
        points=[
            Point(x=20, y=10),
            Point(x=-20, y=10),
            Point(x=0, y=-10),
        ]
    )
    assert is_intersected(t1, t2)

    t2 = Triangle(
        points=[
            Point(x=10, y=0),
            Point(x=-10, y=0),
            Point(x=0, y=0),
        ]
    )
    assert not is_intersected(t1, t2)

    t2 = Triangle(
        points=[
            Point(x=10, y=0),
            Point(x=-10, y=0),
            Point(x=0, y=-1),
        ]
    )
    assert not is_intersected(t1, t2)



def test_rectangle_rectangle_intersection():
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

    r2 = Rectangle(
        left=-2,
        top=-2,
        width=4,
        height=4,
    )
    assert is_intersected(r1, r2)

    r2 = Rectangle(
        left=-10,
        top=-10,
        width=20,
        height=20,
    )
    assert is_intersected(r1, r2)

    r2 = Rectangle(
        left=5,
        top=0,
        width=10,
        height=10,
    )
    assert not is_intersected(r1, r2)

    r2 = Rectangle(
        left=5,
        top=5,
        width=10,
        height=10,
    )
    assert not is_intersected(r1, r2)

    r2 = Rectangle(
        left=10,
        top=10,
        width=10,
        height=10,
    )
    assert not is_intersected(r1, r2)


def test_triangle_circle_intersection():
    pass
