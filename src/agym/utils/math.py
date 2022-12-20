from heapq import heapify, heappop
from typing import Any, Callable, Iterable, List, Optional, Protocol, TypeVar


class IComparable(Protocol):
    def __lt__(self, other) -> bool:
        pass


T = TypeVar("T")


class KeyValueSortPair(IComparable):
    def __init__(self, key: IComparable, value: T) -> None:
        self.key = key
        self.value = value

    def __lt__(self, other) -> bool:
        return self.key < other.key


SortComparator = Callable[[T], IComparable]


def lazy_sorted(
    arr: Iterable[T], key: Optional[SortComparator] = None
) -> Iterable[T]:
    if key is None:
        key = lambda x: x

    heap = [KeyValueSortPair(key=key(x), value=x) for x in arr]
    heapify(heap)

    yield from (heappop(heap).value for _ in range(len(heap)))


def get_n_min(arr: List[float], n: int) -> List[float]:
    heap = [x for x in arr]
    heapify(heap)

    res = [heappop(heap) for _ in range(n)]
    return res


def get_n_max(arr: List[float], n: int) -> List[float]:
    heap = [-x for x in arr]
    heapify(heap)

    res = [-heappop(heap) for _ in range(n)]
    return res
