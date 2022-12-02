from typing import Iterable, Optional

from agym.games.breakout.geom import Rectangle
from agym.games.breakout.geom.kdtree.node import TreeNode
from agym.games.breakout.geom.kdtree.record import Record


def build_record(
    left: float,
    top: float,
    right: float,
    bottom: float,
    item_id: int = 1,
    class_id: int = 1,
) -> Record:
    shape = Rectangle(
        left=left,
        top=top,
        width=right - left,
        height=bottom - top,
    )

    return Record(
        item_id=item_id,
        class_id=class_id,
        shape=shape,
        bounding_box=shape.bounding_box,
    )


def get_depth(node: Optional[TreeNode]) -> int:
    if node is None:
        return 0

    if node.is_leaf:
        return 1

    l = get_depth(node.left)
    m = get_depth(node.middle)
    r = get_depth(node.right)

    return max(l, m, r) + 1


def traveres(node: Optional[TreeNode]) -> Iterable[TreeNode]:
    if node is None:
        return

    yield from traveres(node.left)
    yield node
    yield from traveres(node.middle)
    yield from traveres(node.right)
