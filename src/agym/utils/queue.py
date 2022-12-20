from collections import deque
from typing import Deque, Generic, Iterator, Protocol, TypeVar

T = TypeVar("T")


class IQueue(Generic[T], Protocol):
    def push(self, value: T) -> None:
        pass

    def pop(self) -> T:
        pass

    @property
    def back(self) -> T:
        pass

    @property
    def front(self) -> T:
        pass

    def __len__(self) -> int:
        pass

    def __iter__(self) -> Iterator[T]:
        pass


class Queue(IQueue[T]):
    def __init__(self):
        self._queue: Deque[T] = deque()
        self._size = 0

    def push(self, value: T) -> None:
        self._size += 1
        self._queue.append(value)

    def pop(self) -> T:
        if self._size == 0:
            raise RuntimeError("Queue is empty and value cannot be poped")

        self._size -= 1
        return self._queue.popleft()

    @property
    def back(self) -> T:
        if self._size == 0:
            raise RuntimeError("Queue is empty and has no tail")

        return self._queue[0]

    @property
    def front(self) -> T:
        if self._size == 0:
            raise RuntimeError("Queue is empty and has no front")

        return self._queue[-1]

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        for item in self._queue:
            yield item


class SizedQueue(IQueue[T]):
    def __init__(self, max_size: int) -> None:
        self._max_size = max_size
        self._queue: IQueue[T] = Queue()

    def push(self, value: T) -> None:
        self._queue.push(value)

        if self._size > self._max_size:
            self.pop()

    @property
    def _size(self) -> int:
        return len(self)

    def pop(self) -> T:
        return self._queue.pop()

    @property
    def back(self) -> T:
        return self._queue.back

    @property
    def front(self) -> T:
        return self._queue.front

    def __len__(self) -> int:
        return len(self._queue)

    def __iter__(self) -> Iterator[T]:
        yield from self._queue
