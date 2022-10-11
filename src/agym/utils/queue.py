from collections import deque
from typing import TypeVar, Generic, Iterator

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self):
        self.queue: deque[T] = deque()
        self.size = 0

    def push(self, value: T) -> None:
        self.size += 1
        self.queue.append(value)

    def pop(self) -> T:
        if self.size == 0:
            raise RuntimeError("Queue is empty and value cannot be poped")

        self.size -= 1
        return self.queue.popleft()

    @property
    def back(self) -> T:
        if self.size == 0:
            raise RuntimeError("Queue is empty and has no tail")

        return self.queue[0]

    @property
    def front(self) -> T:
        if self.size == 0:
            raise RuntimeError("Queue is empty and has no front")

        return self.queue[-1]

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[T]:
        for item in self.queue:
            yield item
