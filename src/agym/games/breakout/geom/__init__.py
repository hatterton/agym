from .basic import Line2, Point, Segment, Vec2
from .intersecting import (
    Intersection,
    get_intersection,
    get_intersection_circle_circle,
    get_intersection_circle_segment,
    get_intersection_line_line,
    get_intersection_rectangle_rectangle,
    get_intersection_segment_segment,
    get_intersection_triangle_circle,
    get_intersection_triangle_triangle,
    is_intersected,
)
from .kdtree import ClassId, ItemId, KDTree, Record
from .protocols import SupportsBoundingBox
from .shapes import Circle, Rectangle, Shape, Triangle
