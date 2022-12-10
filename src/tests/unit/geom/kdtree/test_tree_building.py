import pytest

from agym.games.breakout.geom.kdtree import KDTree
from agym.games.breakout.geom.kdtree.node import (
    LeafTreeNode,
    SplitTreeNode,
    TreeNode,
)

from .tree_utils import build_record, get_depth, traveres


@pytest.mark.kdtree
@pytest.mark.tree
class TestTreeBuilding:
    def test_build_one_node(self):
        r = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )

        tree = KDTree(
            records=[r],
        )

        assert len(list(tree.root.generate_items())) == 1
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
        )

        assert len(list(tree.root.generate_items())) == 2
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
        )

        assert len(list(tree.root.generate_items())) == 2
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
        )

        assert len(list(tree.root.generate_items())) == 3
        assert get_depth(tree.root) == 3
        for node in traveres(tree.root):
            assert len(node.items) == 1

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
        )

        assert len(list(tree.root.generate_items())) == 2
        assert get_depth(tree.root) == 2
        for node in traveres(tree.root):
            assert len(node.items) <= 1

    def test_build_two_nodes_nonsplitable(self):
        r1 = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )
        r2 = build_record(
            left=0,
            top=0,
            right=10,
            bottom=10,
        )

        tree = KDTree(
            records=[r1, r2],
            max_depth=5,
        )

        assert len(list(tree.root.generate_items())) == 2
        # TODO strange behaviour
        assert get_depth(tree.root) == 2
        # for node in traveres(tree.root):
        #     assert len(node.items) in [0, 2]

    def test_build_many_nodes_separable(self):
        rs = [
            build_record(
                left=i * 10 + 1,
                right=(i + 1) * 10,
                top=j * 10 + 1,
                bottom=(j + 1) * 10,
            )
            for i in range(2**5)
            for j in range(2**5)
        ]

        tree = KDTree(
            records=rs,
            max_depth=20,
        )

        assert len(list(tree.root.generate_items())) == 2**10
        assert get_depth(tree.root) == 11
        for node in traveres(tree.root):
            assert len(node.items) == 1

    def test_build_many_nodes_separable_max_depth(self):
        rs = [
            build_record(
                left=i * 10 + 1,
                right=(i + 1) * 10,
                top=j * 10 + 1,
                bottom=(j + 1) * 10,
            )
            for i in range(2**5)
            for j in range(2**5)
        ]

        tree = KDTree(
            records=rs,
            max_depth=5,
        )

        assert len(list(tree.root.generate_items())) == 2**10
        assert get_depth(tree.root) == 6

    def test_build_many_nodes_separable_num_records_to_stop(self):
        rs = [
            build_record(
                left=i * 10 + 1,
                right=(i + 1) * 10,
                top=j * 10 + 1,
                bottom=(j + 1) * 10,
            )
            for i in range(2**5)
            for j in range(2**5)
        ]

        tree = KDTree(
            records=rs,
            num_records_stop=2**6,
        )

        assert len(list(tree.root.generate_items())) == 2**10
        assert get_depth(tree.root) == 5
        for node in traveres(tree.root):
            assert len(node.items) == 2**6
