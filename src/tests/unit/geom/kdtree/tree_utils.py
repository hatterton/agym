from typing import Iterable, Optional

from geometry import Rectangle
from geometry.kdtree.node import LeafTreeNode, SplitTreeNode, TreeNode
from geometry.kdtree.record import Record


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

    if isinstance(node, SplitTreeNode):
        l = get_depth(node.left)
        m = get_depth(node.middle)
        r = get_depth(node.right)

        return max(l, m, r) + 1

    return 1


def traveres(node: Optional[TreeNode]) -> Iterable[LeafTreeNode]:
    if node is None:
        return

    if isinstance(node, SplitTreeNode):
        yield from traveres(node.left)
        yield from traveres(node.middle)
        yield from traveres(node.right)

    elif isinstance(node, LeafTreeNode):
        yield node
