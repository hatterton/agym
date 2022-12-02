from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Collection, Iterable, List, Set, Tuple

from ..intersecting import IntersectionStrict, get_intersection
from ..shapes import Rectangle
from .node import CollidablePair, IntersactionInfo, IntersactionPair, TreeNode
from .record import ClassId, ItemId, Record
from .scores import get_score


class BoundType(Enum):
    OPENING = 0
    CLOSING = 1


@dataclass
class RecordInfo:
    bound: float
    idx: int
    bound_type: BoundType


class KDTree:
    def __init__(
        self,
        records: List[Record],
        collidable_pairs: Collection[CollidablePair],
        alpha: float = 0.5,
        max_depth: int = -1,
        num_records_stop: int = 1,
    ) -> None:
        self._collidable_pairs = collidable_pairs

        self._alpha = alpha
        self._max_depth = max_depth
        self._num_records_stop = num_records_stop
        self._records = records

        self.root: TreeNode
        self.build(records)

    def build(self, records: List[Record]) -> None:
        verticals = []
        horizontals = []
        for idx, r in enumerate(records):
            verticals.append(
                RecordInfo(
                    bound=r.bounding_box.left,
                    idx=idx,
                    bound_type=BoundType.OPENING,
                )
            )
            verticals.append(
                RecordInfo(
                    bound=r.bounding_box.right,
                    idx=idx,
                    bound_type=BoundType.CLOSING,
                )
            )

            horizontals.append(
                RecordInfo(
                    bound=r.bounding_box.top,
                    idx=idx,
                    bound_type=BoundType.OPENING,
                )
            )
            horizontals.append(
                RecordInfo(
                    bound=r.bounding_box.bottom,
                    idx=idx,
                    bound_type=BoundType.CLOSING,
                )
            )

        verticals = sorted(
            verticals, key=lambda r: (r.bound, r.bound_type.value)
        )
        horizontals = sorted(
            horizontals, key=lambda r: (r.bound, r.bound_type.value)
        )

        self.root = self._build(
            ids=set(range(len(records))),
            records=records,
            verticals=verticals,
            horizontals=horizontals,
            depth=0,
        )

    def _build(
        self,
        ids: Set[int],
        records: List[Record],
        verticals: List[RecordInfo],
        horizontals: List[RecordInfo],
        depth: int,
    ) -> TreeNode:
        if depth == self._max_depth or len(ids) <= self._num_records_stop:
            return TreeNode(items=[records[idx] for idx in ids])

        vscores = self._calculate_bound_scores(
            bounds=verticals,
            num_total=len(ids),
        )
        hscores = self._calculate_bound_scores(
            bounds=horizontals,
            num_total=len(ids),
        )

        max_vscore = max(vscores)
        max_hscore = max(hscores)

        if max_vscore > max_hscore:
            bounds = verticals
            max_idx = vscores.index(max_vscore)
        else:
            bounds = horizontals
            max_idx = hscores.index(max_hscore)

        left_ids = set()
        middle_ids = set()
        right_ids = set(ids)
        for idx, b in enumerate(bounds):
            if b.bound_type == BoundType.OPENING:
                right_ids.remove(b.idx)
                middle_ids.add(b.idx)

            elif b.bound_type == BoundType.CLOSING:
                middle_ids.remove(b.idx)
                left_ids.add(b.idx)

            if idx == max_idx:
                break

        left = (
            self._build(
                ids=left_ids,
                records=records,
                verticals=[b for b in verticals if b.idx in left_ids],
                horizontals=[b for b in horizontals if b.idx in left_ids],
                depth=depth + 1,
            )
            if left_ids
            else None
        )

        middle = (
            self._build(
                ids=middle_ids,
                records=records,
                verticals=[b for b in verticals if b.idx in middle_ids],
                horizontals=[b for b in horizontals if b.idx in middle_ids],
                depth=depth + 1,
            )
            if middle_ids
            else None
        )

        right = (
            self._build(
                ids=right_ids,
                records=records,
                verticals=[b for b in verticals if b.idx in right_ids],
                horizontals=[b for b in horizontals if b.idx in right_ids],
                depth=depth + 1,
            )
            if right_ids
            else None
        )

        return TreeNode(
            left=left,
            middle=middle,
            right=right,
        )

    def _calculate_bound_scores(
        self, bounds: List[RecordInfo], num_total: int
    ) -> List[float]:
        num_open = 0
        num_closed = 0

        scores = []
        for idx, b in enumerate(bounds):
            if idx == len(bounds) - 1:
                break

            if b.bound_type == BoundType.OPENING:
                num_open += 1

            elif b.bound_type == BoundType.CLOSING:
                num_open -= 1
                num_closed += 1

            score = get_score(
                l=num_closed,
                m=num_open,
                r=num_total - num_closed - num_open,
                alpha=self._alpha,
            )
            scores.append(score)

        return scores

    def generate_colliding_items(
        self,
    ) -> Iterable[IntersactionInfo]:
        # yield from self._naive_generate_colliding_items(self._records)
        # return

        yield from self._generate_colliding_items(
            node=self.root,
        )

    def _generate_colliding_items(
        self,
        node: TreeNode,
    ) -> Iterable[IntersactionInfo]:
        yield from node.generate_intersections(
            collidable_pairs=self._collidable_pairs,
        )

    def _naive_generate_colliding_items(
        self, records: List[Record]
    ) -> Iterable[Tuple[Tuple[ItemId, ItemId], IntersectionStrict]]:
        collided_ids = set()

        for r1, r2 in combinations(records, 2):
            idx1 = r1.item_id
            idx2 = r2.item_id

            if idx1 == idx2:
                continue

            if (idx1, idx2) in collided_ids or (idx2, idx1) in collided_ids:
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
