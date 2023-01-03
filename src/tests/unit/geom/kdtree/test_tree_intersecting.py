import pytest

from geometry import Circle, Point
from geometry.kdtree import KDTree
from geometry.kdtree.node import Record

from .tree_utils import build_record


@pytest.mark.kdtree
@pytest.mark.tree
class TestTree:
    def test_intersecting_two_nodes__positive(self):
        r1 = build_record(
            left=0,
            top=0,
            right=5,
            bottom=5,
            item_id=1,
            class_id=1,
        )
        r2 = build_record(
            left=4,
            top=4,
            right=9,
            bottom=9,
            item_id=2,
            class_id=1,
        )
        rs = [r1, r2]
        collidable_pairs = {(1, 1)}

        tree = KDTree(
            records=rs,
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 1

    def test_intersecting_two_nodes__the_same_item_id__negative(self):
        r1 = build_record(
            left=0,
            top=0,
            right=5,
            bottom=5,
            item_id=1,
            class_id=1,
        )
        r2 = build_record(
            left=4,
            top=4,
            right=9,
            bottom=9,
            item_id=1,
            class_id=1,
        )
        rs = [r1, r2]
        collidable_pairs = {(1, 1)}

        tree = KDTree(
            records=rs,
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 0

    def test_intersecting_two_nodes__non_colladable_class_id__negative(self):
        r1 = build_record(
            left=0,
            top=0,
            right=5,
            bottom=5,
            item_id=1,
            class_id=1,
        )
        r2 = build_record(
            left=4,
            top=4,
            right=9,
            bottom=9,
            item_id=2,
            class_id=1,
        )
        rs = [r1, r2]
        collidable_pairs = {(1, 2)}

        tree = KDTree(
            records=rs,
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 0

    def test_intersecting_two_nodes__seperable_rectangles__negative(self):
        r1 = build_record(
            left=0,
            top=0,
            right=5,
            bottom=5,
            item_id=1,
            class_id=1,
        )
        r2 = build_record(
            left=6,
            top=6,
            right=11,
            bottom=11,
            item_id=2,
            class_id=1,
        )
        rs = [r1, r2]
        collidable_pairs = {(1, 1)}

        tree = KDTree(
            records=rs,
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 0

    def test_intersecting_two_nodes__not_intersecting_shapes__negative(self):
        s1 = Circle(
            center=Point(x=2.5, y=2.5),
            radius=2.5,
        )
        s2 = Circle(
            center=Point(x=6.5, y=6.5),
            radius=2.5,
        )

        r1 = Record(
            item_id=1,
            class_id=1,
            shape=s1,
            bounding_box=s1.bounding_box,
        )
        r2 = Record(
            item_id=2,
            class_id=1,
            shape=s2,
            bounding_box=s2.bounding_box,
        )
        rs = [r1, r2]
        collidable_pairs = {(1, 2)}

        tree = KDTree(
            records=rs,
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 0

    def test_intersecting_nums__none(self):
        rs = [
            build_record(
                left=i * 10,
                right=(i + 1) * 10 - 1,
                top=j * 10,
                bottom=(j + 1) * 10 - 1,
                item_id=i * 10 + j,
                class_id=1,
            )
            for i in range(10)
            for j in range(10)
        ]
        collidable_pairs = {(1, 1)}

        tree = KDTree(
            records=rs,
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 0

    def test_intersecting_nums__one(self):
        rs = [
            build_record(
                left=i * 10,
                right=(i + 1) * 10 - 1,
                top=j * 10,
                bottom=(j + 1) * 10 - 1,
                item_id=i * 10 + j,
                class_id=1,
            )
            for i in range(10)
            for j in range(10)
        ]
        collidable_pairs = {(1, 1)}
        r = build_record(
            left=5,
            top=5,
            right=6,  # TODO strange behaviour with rectangle null area
            bottom=6,  # TODO strange behaviour with rectangle null area
            item_id=-1,
            class_id=1,
        )

        tree = KDTree(
            records=rs + [r],
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 1

    def test_intersecting_nums_full(self):
        rs = [
            build_record(
                left=i * 10,
                right=(i + 1) * 10 - 1,
                top=j * 10,
                bottom=(j + 1) * 10 - 1,
                item_id=j * 10 + i,
                class_id=1,
            )
            for i in range(10)
            for j in range(10)
        ]
        collidable_pairs = {(1, 1)}
        r = build_record(
            left=0,
            top=0,
            right=100,
            bottom=100,
            item_id=-1,
            class_id=1,
        )

        tree = KDTree(
            records=rs + [r],
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 100

    def test_intersecting_nums__part(self):
        rs = [
            build_record(
                left=i * 10,
                right=(i + 1) * 10 - 1,
                top=j * 10,
                bottom=(j + 1) * 10 - 1,
                item_id=j * 10 + i,
                class_id=1,
            )
            for i in range(10)
            for j in range(10)
        ]
        collidable_pairs = {(1, 1)}
        r = build_record(
            left=0,
            top=0,
            right=35,
            bottom=75,
            item_id=-1,
            class_id=1,
        )

        tree = KDTree(
            records=rs + [r],
        )

        intesections = list(tree.generate_colliding_items(collidable_pairs))
        assert len(intesections) == 32
