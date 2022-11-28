from heapq import heapify, heappop
from typing import List


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
