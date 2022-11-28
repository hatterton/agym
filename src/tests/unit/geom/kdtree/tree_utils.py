from typing import Iterable, Optional

from agym.games.breakout.geom.kdtree.node import TreeNode


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
