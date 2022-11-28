import pytest

from agym.games.breakout.geom.kdtree.node import TreeNode
from agym.games.breakout.geom.kdtree.record import Record
from agym.games.breakout.geom import Rectangle

from .tree_utils import get_depth, traveres


def build_record(left: float, top: float, right: float, bottom: float) -> Record:
    shape = Rectangle(
        left=left,
        top=top,
        width=right-left,
        height=bottom-top,
    )

    return Record(
        item_id=1,
        class_id=1,
        shape=shape,
        bounding_box=shape.bounding_box,
    )

def rect_contains(outer: Rectangle, inner: Rectangle) -> bool:
    return (
        outer.left <= inner.left and
        outer.right >= inner.right and
        outer.top <= inner.top and
        outer.bottom >= inner.bottom
    )


@pytest.mark.kdtree
@pytest.mark.node
class TestTreeNode:
    def test_bounding_box(self):
        r1 = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )
        r2 = build_record(
            left=10,
            top=10,
            right=15,
            bottom=15,
        )

        node = TreeNode(
            items=[r1, r2],
        )

        assert rect_contains(node.bounding_box, r1.bounding_box)
        assert rect_contains(node.bounding_box, r2.bounding_box)

    def test_depth(self):
        r = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )

        node = TreeNode(
            left=TreeNode(
                left=TreeNode(
                    items=[r],
                ),
                middle=None,
                right=TreeNode(
                    items=[r],
                ),
            ),
            middle=TreeNode(
                items=[r, r],
            ),
            right=TreeNode(
                items=[r],
            ),
        )

        assert get_depth(node) == 3

    def test_traveres(self):
        r = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )

        node = TreeNode(
            left=TreeNode(
                left=TreeNode(
                    items=[r],
                ),
                middle=None,
                right=TreeNode(
                    items=[r],
                ),
            ),
            middle=TreeNode(
                items=[r, r],
            ),
            right=TreeNode(
                items=[r],
            ),
        )

        expected_items = [1, 0, 1, 0, 2, 1]
        nodes = list(traveres(node))
        assert len(expected_items) == len(nodes)

        for node, num_items in zip(nodes, expected_items):
            assert len(node.items) == num_items


    def test_item_iterations(self):
        r = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )

        node = TreeNode(
            left=TreeNode(
                left=TreeNode(
                    items=[r],
                ),
                middle=None,
                right=TreeNode(
                    items=[r],
                ),
            ),
            middle=TreeNode(
                items=[r, r],
            ),
            right=TreeNode(
                items=[r],
            ),
        )

        items = list(node)
        assert len(items) == 5
