from dataclasses import dataclass, field
from functools import cached_property
from typing import Collection, Iterable, Iterator, List, Optional, Set, Tuple

from ..intersecting import IntersectionStrict, get_intersection
from ..shapes import Rectangle
from .record import ClassId, ItemId, Record


@dataclass
class TreeNode:
    left: "Optional[TreeNode]" = None
    right: "Optional[TreeNode]" = None
    middle: "Optional[TreeNode]" = None

    items: List[Record] = field(default_factory=list)

    @cached_property
    def bounding_box(self) -> Rectangle:
        records = iter(self)

        record = next(records)
        bbox = record.bounding_box

        for record in records:
            bbox = bbox.union(record.bounding_box)

        return bbox

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None and self.middle is None

    def generate_intersecting(
        self,
        record: Record,
        pairs: Collection[Tuple[ClassId, ClassId]],
        collided: Set[Tuple[ItemId, ItemId]],
    ) -> Iterable[Tuple[Tuple[ItemId, ItemId], IntersectionStrict]]:
        if not self.bounding_box.is_intersected(record.bounding_box):
            return []

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

            if (class1, class2) not in pairs:
                continue

            if item.bounding_box.is_intersected(record.bounding_box):
                continue

            intersection = get_intersection(record.shape, item.shape)
            if intersection is None:
                continue

            collided.add((idx1, idx2))

            yield (idx1, idx2), intersection

        if self.left is not None:
            yield from self.left.generate_intersecting(
                record=record,
                pairs=pairs,
                collided=collided,
            )

        if self.middle is not None:
            yield from self.middle.generate_intersecting(
                record=record,
                pairs=pairs,
                collided=collided,
            )

        if self.right is not None:
            yield from self.right.generate_intersecting(
                record=record,
                pairs=pairs,
                collided=collided,
            )

    def __iter__(self) -> Iterator[Record]:
        yield from self.items

        if self.left is not None:
            yield from self.left

        if self.middle is not None:
            yield from self.middle

        if self.right is not None:
            yield from self.right
