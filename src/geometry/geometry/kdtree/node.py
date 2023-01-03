from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import cached_property
from typing import Collection, Iterable, Iterator, List, Optional, Set, Tuple

from ..intersecting import IntersectionStrict, get_intersection
from ..shapes import Rectangle
from .record import ClassId, ItemId, Record

IntersactionPair = Tuple[ItemId, ItemId]
CollidablePair = Tuple[ClassId, ClassId]
IntersactionInfo = Tuple[IntersactionPair, IntersectionStrict]


class TreeNodeType(Enum):
    LEAF = auto()
    VERTICAL = auto()
    HORISONTAL = auto()


class ParentRelativeType(Enum):
    ROOT = auto()
    LEFT = auto()
    RIGHT = auto()
    MIDDLE = auto()


@dataclass
class TreeNode(ABC):
    type: TreeNodeType
    parent_relative: ParentRelativeType

    @abstractproperty
    def bounding_box(self) -> Rectangle:
        pass

    @property
    def is_leaf(self) -> bool:
        return self.type == TreeNodeType.LEAF

    @staticmethod
    def _generate_intersactions_robust(
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

    @abstractmethod
    def _generate_intersections(
        self,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        pass

    @staticmethod
    def _generate_record_intersections_robust(
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

        if not self.bounding_box.is_intersected(record.bounding_box):
            return

        yield from self._generate_record_intersections(
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    @abstractmethod
    def _generate_record_intersections(
        self,
        record: Record,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        pass

    @staticmethod
    def _generate_items_robust(
        node: "Optional[TreeNode]",
    ) -> Iterable[Record]:
        if node is None:
            return

        yield from node.generate_items()

    def generate_items(self) -> Iterator[Record]:
        yield from self._generate_items()

    @abstractmethod
    def _generate_items(self) -> Iterator[Record]:
        pass

    @staticmethod
    def _traverse_subnodes_robust(
        node: "Optional[TreeNode]",
    ) -> "Iterable[TreeNode]":
        if node is None:
            return

        yield from node.traverse_subnodes()

    def traverse_subnodes(
        self,
    ) -> "Iterable[TreeNode]":
        yield from self._traverse_subnodes()

    @abstractmethod
    def _traverse_subnodes(
        self,
    ) -> "Iterable[TreeNode]":
        pass


@dataclass
class LeafTreeNode(TreeNode):
    items: List[Record] = field(default_factory=list)

    @cached_property
    def bounding_box(self) -> Rectangle:
        bboxes = [item.bounding_box for item in self.items]

        bbox_iter = iter(bboxes)
        bbox = next(bbox_iter)

        for b in bbox_iter:
            bbox = bbox.union(b)

        return bbox

    def _generate_intersections(
        self,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        for record in self.items:
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

    def _generate_items(self) -> Iterator[Record]:
        yield from self.items

    def _traverse_subnodes(
        self,
    ) -> "Iterable[TreeNode]":
        yield self


@dataclass
class SplitTreeNode(TreeNode):
    threashold: float

    left: "Optional[TreeNode]" = None
    right: "Optional[TreeNode]" = None
    middle: "Optional[TreeNode]" = None

    @cached_property
    def bounding_box(self) -> Rectangle:
        subnodes = [self.left, self.middle, self.right]
        bboxes = [node.bounding_box for node in subnodes if node is not None]

        bbox_iter = iter(bboxes)
        bbox = next(bbox_iter)

        for b in bbox_iter:
            bbox = bbox.union(b)

        return bbox

    def _generate_intersections(
        self,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        for record in self._generate_items_robust(self.middle):
            yield from self._generate_record_intersections_robust(
                node=self.left,
                record=record,
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

            yield from self._generate_record_intersections_robust(
                node=self.right,
                record=record,
                collidable_pairs=collidable_pairs,
                collided=collided,
            )

        yield from self._generate_intersactions_robust(
            node=self.left,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

        yield from self._generate_intersactions_robust(
            node=self.middle,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

        yield from self._generate_intersactions_robust(
            node=self.right,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    def _generate_record_intersections(
        self,
        record: Record,
        collidable_pairs: Collection[CollidablePair],
        collided: Set[IntersactionPair],
    ) -> Iterable[IntersactionInfo]:
        yield from self._generate_record_intersections_robust(
            node=self.left,
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

        yield from self._generate_record_intersections_robust(
            node=self.middle,
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

        yield from self._generate_record_intersections_robust(
            node=self.right,
            record=record,
            collidable_pairs=collidable_pairs,
            collided=collided,
        )

    def _generate_items(self) -> Iterator[Record]:
        yield from self._generate_items_robust(self.left)
        yield from self._generate_items_robust(self.middle)
        yield from self._generate_items_robust(self.right)

    def _traverse_subnodes(
        self,
    ) -> "Iterable[TreeNode]":
        yield self

        yield from self._traverse_subnodes_robust(self.left)
        yield from self._traverse_subnodes_robust(self.middle)
        yield from self._traverse_subnodes_robust(self.right)
