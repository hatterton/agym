from typing import (
    Iterable,
    Tuple,
)
from itertools import combinations

from ..shapes import Rectangle
from .record import (
    Record,
    ItemId,
)
from ..intersecting import (
    get_intersection,
    IntersectionStrict,
)


class KDTree:
    def __init__(self, records: Iterable[Record], alpha: float) -> None:
        self._alpha = alpha
        self._records = records

    def generate_colliding_items(self) -> Iterable[Tuple[Tuple[ItemId, ItemId], IntersectionStrict]]:
        collided_ids = set()

        for r1, r2 in combinations(self._records, 2):
            idx1 = min(r1.item_id, r2.item_id)
            idx2 = max(r1.item_id, r2.item_id)

            if idx1 == idx2:
                continue

            if (idx1, idx2) in collided_ids:
                continue

            if not r1.bounding_box.is_intersected(r2.bounding_box):
                continue

            intersection = get_intersection(r1.shape, r2.shape)
            if intersection is None:
                continue

            collided_ids.add((idx1, idx2))

            yield (idx1, idx2), intersection
