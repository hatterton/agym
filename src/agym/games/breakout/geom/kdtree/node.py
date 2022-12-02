from dataclasses import dataclass, field
from functools import cached_property
from typing import (
    Collection,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    cast,
)

from ..intersecting import IntersectionStrict, get_intersection
from ..shapes import Rectangle
from .record import ClassId, ItemId, Record

IntersactionPair = Tuple[ItemId, ItemId]
CollidablePair = Tuple[ClassId, ClassId]
IntersactionInfo = Tuple[IntersactionPair, IntersectionStrict]


@dataclass
class TreeNode:
    left: "Optional[TreeNode]" = None
    right: "Optional[TreeNode]" = None
    middle: "Optional[TreeNode]" = None

    items: List[Record] = field(default_factory=list)

    @cached_property
    def bounding_box(self) -> Rectangle:
        bboxes: List[Rectangle]
        if self.items:
            bboxes = [item.bounding_box for item in self.items]

        else:
            subnodes = [self.left, self.middle, self.right]
            bboxes = [
                node.bounding_box for node in subnodes if node is not None
            ]

        bbox_iter = iter(bboxes)
        bbox = next(bbox_iter)

        for b in bbox_iter:
            bbox = bbox.union(b)

        return bbox

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None and self.middle is None

    @staticmethod
    def generate_intersections_robust(
        node: "Optional[TreeNode]",
        collidable_pairs: Collection[Tuple[ClassId, ClassId]],
        collided: Optional[Set[IntersactionPair]] = None,
    ) -> Iterable[IntersactionInfo]:
        if node is None:
            return

        yield from node.generate_intersections(
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    def generate_intersections(
        self,
        collidable_pairs: Collection[Tuple[ClassId, ClassId]],
        collided: Optional[Set[IntersactionPair]] = None,
    ) -> Iterable[IntersactionInfo]:
        if collided is None:
            collided = set()

        yield from self._generate_intersections(
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    def _generate_intersections(
        self,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        if self.items:
            yield from self._generate_self_intersactions(
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

        else:
            yield from self._generate_subnodes_intersections(
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

    def _generate_self_intersactions(
        self,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        for record in self.items:
            yield from self._generate_record_self_intersections(
                record=record,
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

    def _generate_subnodes_intersections(
        self,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        for record in self.generate_items_robust(self.middle):
            yield from self.generate_record_intersections_robust(
                node=self.left,
                record=record,
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

            yield from self.generate_record_intersections_robust(
                node=self.right,
                record=record,
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

        yield from self.generate_intersections_robust(
            node=self.left,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

        yield from self.generate_intersections_robust(
            node=self.middle,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

        yield from self.generate_intersections_robust(
            node=self.right,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    @staticmethod
    def generate_record_intersections_robust(
        node: "Optional[TreeNode]",
        record: Record,
        collidable_pairs: Collection[CollidablePair],
        collided: Optional[Set[IntersactionPair]] = None,
    ) -> Iterable[IntersactionInfo]:
        if node is None:
            return

        yield from node.generate_record_intersections(
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    def generate_record_intersections(
        self,
        record: Record,
        collidable_pairs: Collection[CollidablePair],
        collided: Optional[Set[IntersactionPair]] = None,
    ) -> Iterable[IntersactionInfo]:
        if collided is None:
            collided = set()

        yield from self._generate_record_intersections(
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    def _generate_record_intersections(
        self,
        record: Record,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        if not self.bounding_box.is_intersected(record.bounding_box):
            return

        if self.items:
            yield from self._generate_record_self_intersections(
                record=record,
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

        else:
            yield from self._generate_record_subnodes_intersections(
                record=record,
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

    def _generate_record_self_intersections(
        self,
        record: Record,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        for item in self.items:
            idx1 = record.item_id
            idx2 = item.item_id

            if idx1 == idx2:
                continue

            if (idx1, idx2) in collided or (idx2, idx1) in collided:
                continue

            class1 = record.class_id
            class2 = item.class_id

            if class1 > class2:
                idx1, idx2 = idx2, idx1
                class1, class2 = class2, class1

            if (class1, class2) not in collidable_pairs:
                continue

            if not item.bounding_box.is_intersected(record.bounding_box):
                continue

            intersection = get_intersection(record.shape, item.shape)
            if intersection is None:
                continue

            collided.add((idx1, idx2))

            yield (idx1, idx2), intersection

    def _generate_record_subnodes_intersections(
        self,
        record: Record,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        yield from self.generate_record_intersections_robust(
            node=self.left,
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

        yield from self.generate_record_intersections_robust(
            node=self.middle,
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

        yield from self.generate_record_intersections_robust(
            node=self.right,
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    @staticmethod
    def generate_items_robust(
        node: "Optional[TreeNode]",
    ) -> Iterable[Record]:
        if node is None:
            return

        yield from node

    def __iter__(self) -> Iterator[Record]:
        if self.items:
            yield from self.items

        else:
            yield from self.generate_items_robust(self.left)
            yield from self.generate_items_robust(self.middle)
            yield from self.generate_items_robust(self.right)
