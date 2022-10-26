from typing import (
    Iterable,
    Tuple,
    Collection,
)
from itertools import combinations

from ..shapes import Rectangle
from .record import (
    Record,
    ItemId,
    ClassId,
)
from ..intersecting import (
    get_intersection,
    IntersectionStrict,
)


class KDTree:
    def __init__(self, records: Iterable[Record], alpha: float, collidable_pairs: Collection[Tuple[ClassId, ClassId]]) -> None:
        self._alpha = alpha
        self._records = records
        self._collidable_pairs = collidable_pairs

    def generate_colliding_items(self) -> Iterable[Tuple[Tuple[ItemId, ItemId], IntersectionStrict]]:
        collided_ids = set()

        for r1, r2 in combinations(self._records, 2):
            idx1 = r1.item_id
            idx2 = r2.item_id

            if idx1 == idx2:
                continue

            if (idx1, idx2) in collided_ids:
                continue

            class1 = r1.class_id
            class2 = r2.class_id

            if class1 > class2:
                idx1, idx2 = idx2, idx1
                class1, class2 = class2, class1

            if (class1, class2) not in self._collidable_pairs:
                continue

            if not r1.bounding_box.is_intersected(r2.bounding_box):
                continue

            intersection = get_intersection(r1.shape, r2.shape)
            if intersection is None:
                continue

            collided_ids.add((idx1, idx2))

            yield (idx1, idx2), intersection
