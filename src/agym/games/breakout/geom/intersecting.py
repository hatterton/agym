from typing import Union, Optional
from itertools import product

from .basic import (
    Point,
    Vec2,
    Segment,
    Line2,
)
from .shapes import (
    Triangle,
    Rectangle,
    Circle,
    Shape,
)


IntersectionStrict = Point
Intersection = Optional[IntersectionStrict]


def is_intersected(a: Shape, b: Shape) -> bool:
    intersection = get_intersection(a, b)

    return intersection is not None


def get_intersection(a: Shape, b: Shape) -> Intersection:
    if isinstance(a, Rectangle) and isinstance(b, Rectangle):
        return get_intersection_rectangle_rectangle(a, b)

    elif isinstance(a, Triangle) and isinstance(b, Triangle):
        return get_intersection_triangle_triangle(a, b)

    elif isinstance(a, Circle) and isinstance(b, Circle):
        return get_intersection_circle_circle(a, b)

    elif isinstance(a, Triangle) and isinstance(b, Circle):
        return get_intersection_triangle_circle(a, b)

    elif isinstance(a, Circle) and isinstance(b, Triangle):
        return get_intersection_triangle_circle(b, a)

    raise NotImplementedError(
        "Getting intersection between {} and {} is not supported".format(
            a.__class__.__name__,
            b.__class__.__name__,
        )
    )


def get_intersection_rectangle_rectangle(a: Rectangle, b: Rectangle) -> Intersection:
    inter = intersect_rectangles(a, b)

    if inter.width <= 0 or inter.height <= 0:
        return None

    return inter.center


def get_intersection_triangle_triangle(a: Triangle, b: Triangle) -> Intersection:
    for p in [*a.points, a.center]:
        if is_point_in_triangle(p, b):
            return p

    for p in [*b.points, b.center]:
        if is_point_in_triangle(p, a):
            return p

    for seg1, seg2 in product(a.segments, b.segments):
        intersection = get_intersection_segment_segment(seg1, seg2)

        if intersection is not None:
            return intersection

    return None


def get_intersection_circle_circle(a: Circle, b: Circle) -> Intersection:
    s = a.center - b.center
    sd = s.x ** 2 + s.y ** 2
    sr = (a.radius + b.radius) ** 2

    if sd < sr:
        return (a.center + b.center) / 2
    else:
        return None


def get_intersection_triangle_circle(t: Triangle, c: Circle) -> Intersection:
    if is_point_in_triangle(c.center, t):
        return c.center

    for seg in t.segments:
        intersection = get_intersection_circle_segment(c, seg)

        if intersection is not None:
            return intersection

    return None


def get_intersection_segment_segment(a: Segment, b: Segment) -> Intersection:
    a_line = a.line
    b_line = b.line

    if is_on_same_side(b.begin, b.end, a_line):
        return None

    if is_on_same_side(a.begin, a.end, b_line):
        return None

    return get_intersection_line_line(a_line, b_line)


def get_intersection_line_line(l1: Line2, l2: Line2) -> Intersection:
    d = l2.b * l1.a - l1.b * l2.a
    if d == 0:
        return None

    x = -(l2.b * l1.c - l1.b * l2.c) / d
    y = (l2.a * l1.c - l1.a * l2.c) / d

    return Point(x=x, y=y)


def is_point_in_triangle(p: Point, t: Triangle) -> bool:
    c = t.center

    for seg in t.segments:
        if not is_on_same_side_strict(p, c, seg.line):
            return False

    return True


def is_on_same_side(a: Point, b: Point, l: Line2) -> bool:
    return l.place(a) * l.place(b) >= 0


def is_on_same_side_strict(a: Point, b: Point, l: Line2) -> bool:
    return l.place(a) * l.place(b) > 0


def intersect_rectangles(a: Rectangle, b: Rectangle) -> Rectangle:
    left = max(a.left, b.left)
    right = min(a.right, b.right)
    top = max(a.top, b.top)
    bottom = min(a.bottom, b.bottom)

    return Rectangle(
        left=left,
        top=top,
        width=right-left,
        height=bottom-top,
    )


def get_intersection_circle_segment(c: Circle, s: Segment) -> Intersection:
    # print()
    # print(c)
    # print(s)
    for p in [s.begin, s.end]:
        diff = c.center - p
        sd = diff.x ** 2 + diff.y ** 2
        sr = c.radius ** 2

        if sd < sr:
            return p

    s_line = s.line
    # print(s_line)
    den = s_line.a ** 2 + s_line.b ** 2
    t = - s_line.place(c.center) / den
    n = s_line.normal
    # n /= n.norm()

    # print(n)
    # print(t)
    pr = c.center + n * t

    left = min(s.begin.x, s.end.x)
    right = max(s.begin.x, s.end.x)
    top = min(s.begin.y, s.end.y)
    bottom = max(s.begin.y, s.end.y)
    area = Rectangle(
        left=left,
        top=top,
        width=right-left,
        height=bottom-top,
    )

    if not area.contains(pr):
        return None

    dist = abs(t) * den ** 0.5

    if dist < c.radius:
        return pr
    else:
        return None
