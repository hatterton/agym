from dataclasses import dataclass, field
from typing import (
    List,
    Iterable,
    Iterator,
    Tuple,
    Optional,
)
from functools import cached_property

from ..shapes import Rectangle
from .record import Record


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
        return (
            self.left is None and
            self.right is None and
            self.middle is None
        )

    def __iter__(self) -> Iterator[Record]:
        yield from self.items

        if self.left is not None:
            yield from self.left

        if self.middle is not None:
            yield from self.middle

        if self.right is not None:
            yield from self.right

