import pytest

from agym.games.breakout.geom import Rectangle
from agym.games.breakout.geom.kdtree import KDTree
from agym.games.breakout.geom.kdtree.node import TreeNode
from agym.games.breakout.geom.kdtree.record import Record

from .tree_utils import get_depth, traveres


def build_record(
    left: float, top: float, right: float, bottom: float
) -> Record:
    shape = Rectangle(
        left=left,
        top=top,
        width=right - left,
        height=bottom - top,
    )

    return Record(
        item_id=1,
        class_id=1,
        shape=shape,
        bounding_box=shape.bounding_box,
    )


@pytest.mark.kdtree
@pytest.mark.tree
class TestTree:
    def test_build_one_node(self):
        r = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )

        tree = KDTree(
            records=[r],
            collidable_pairs={},
        )

        assert get_depth(tree.root) == 1
        for node in traveres(tree.root):
            assert len(node.items) <= 1

    def test_build_two_nodes_vertical_separable(self):
        r1 = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )
        r2 = build_record(
            left=11,
            top=0,
            right=21,
            bottom=10,
        )

        tree = KDTree(
            records=[r1, r2],
            collidable_pairs={},
        )

        assert get_depth(tree.root) == 2
        for node in traveres(tree.root):
            assert len(node.items) <= 1

    def test_build_two_nodes_horisontal_separable(self):
        r1 = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )
        r2 = build_record(
            left=0,
            top=11,
            right=10,
            bottom=21,
        )

        tree = KDTree(
            records=[r1, r2],
            collidable_pairs={},
        )

        assert get_depth(tree.root) == 2
        for node in traveres(tree.root):
            assert len(node.items) <= 1

    def test_build_three_nodes_separable(self):
        r1 = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )
        r2 = build_record(
            left=0,
            top=11,
            right=10,
            bottom=21,
        )
        r3 = build_record(
            left=11,
            top=0,
            right=21,
            bottom=21,
        )

        tree = KDTree(
            records=[r1, r2, r3],
            collidable_pairs={},
        )

        assert get_depth(tree.root) == 3
        for node in traveres(tree.root):
            assert len(node.items) <= 1

    def test_build_two_nodes_nonseparable(self):
        r1 = build_record(
            left=0,
            top=1,
            right=10,
            bottom=11,
        )
        r2 = build_record(
            left=9,
            top=10,
            right=19,
            bottom=20,
        )

        tree = KDTree(
            records=[r1, r2],
            collidable_pairs={},
        )

        # print()
        # from pprint import pprint
        # for node in traveres(tree.root):
        #     pprint(node)

        assert get_depth(tree.root) == 2
        for node in traveres(tree.root):
            assert len(node.items) <= 1
