import pytest

from geometry import Rectangle
from geometry.kdtree.node import (
    LeafTreeNode,
    ParentRelativeType,
    SplitTreeNode,
    TreeNode,
    TreeNodeType,
)
from geometry.kdtree.record import Record

from .tree_utils import build_record, get_depth, traveres


def rect_contains(outer: Rectangle, inner: Rectangle) -> bool:
    return (
        outer.left <= inner.left
        and outer.right >= inner.right
        and outer.top <= inner.top
        and outer.bottom >= inner.bottom
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

        node = LeafTreeNode(
            type=TreeNodeType.LEAF,
            parent_relative=ParentRelativeType.ROOT,
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

        node = SplitTreeNode(
            type=TreeNodeType.HORISONTAL,
            parent_relative=ParentRelativeType.ROOT,
            threashold=0.0,
            left=SplitTreeNode(
                type=TreeNodeType.HORISONTAL,
                parent_relative=ParentRelativeType.LEFT,
                threashold=0.0,
                left=LeafTreeNode(
                    type=TreeNodeType.LEAF,
                    parent_relative=ParentRelativeType.LEFT,
                    items=[r],
                ),
                middle=None,
                right=LeafTreeNode(
                    type=TreeNodeType.LEAF,
                    parent_relative=ParentRelativeType.RIGHT,
                    items=[r],
                ),
            ),
            middle=LeafTreeNode(
                type=TreeNodeType.LEAF,
                parent_relative=ParentRelativeType.MIDDLE,
                items=[r, r],
            ),
            right=LeafTreeNode(
                type=TreeNodeType.LEAF,
                parent_relative=ParentRelativeType.RIGHT,
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

        node: TreeNode = SplitTreeNode(
            type=TreeNodeType.LEAF,
            parent_relative=ParentRelativeType.MIDDLE,
            threashold=0.0,
            left=SplitTreeNode(
                type=TreeNodeType.LEAF,
                parent_relative=ParentRelativeType.MIDDLE,
                threashold=0.0,
                left=LeafTreeNode(
                    type=TreeNodeType.LEAF,
                    parent_relative=ParentRelativeType.LEFT,
                    items=[r],
                ),
                middle=None,
                right=LeafTreeNode(
                    type=TreeNodeType.LEAF,
                    parent_relative=ParentRelativeType.RIGHT,
                    items=[r],
                ),
            ),
            middle=LeafTreeNode(
                type=TreeNodeType.LEAF,
                parent_relative=ParentRelativeType.MIDDLE,
                items=[r, r],
            ),
            right=LeafTreeNode(
                type=TreeNodeType.LEAF,
                parent_relative=ParentRelativeType.RIGHT,
                items=[r],
            ),
        )

        expected_items = [1, 1, 2, 1]
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

        node: TreeNode = SplitTreeNode(
            type=TreeNodeType.LEAF,
            parent_relative=ParentRelativeType.MIDDLE,
            threashold=0.0,
            left=SplitTreeNode(
                type=TreeNodeType.LEAF,
                parent_relative=ParentRelativeType.MIDDLE,
                threashold=0.0,
                left=LeafTreeNode(
                    type=TreeNodeType.LEAF,
                    parent_relative=ParentRelativeType.LEFT,
                    items=[r],
                ),
                middle=None,
                right=LeafTreeNode(
                    type=TreeNodeType.LEAF,
                    parent_relative=ParentRelativeType.RIGHT,
                    items=[r],
                ),
            ),
            middle=LeafTreeNode(
                type=TreeNodeType.LEAF,
                parent_relative=ParentRelativeType.MIDDLE,
                items=[r, r],
            ),
            right=LeafTreeNode(
                type=TreeNodeType.LEAF,
                parent_relative=ParentRelativeType.RIGHT,
                items=[r],
            ),
        )

        items = list(node.generate_items())
        assert len(items) == 5
