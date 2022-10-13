from typing import (
    List,
    Iterable,
    # Generic,
    TypeVar,
    Collection,
    Iterator,
)

T = TypeVar("T")

class CachedCollection(Iterable[T]):
    def __init__(self, it: Iterable[T]) -> None:
        self._it = iter(it)
        self._values: List[T] = []

    def __iter__(self) -> Iterator[T]:
        yield from self._values

        try:
            while True:
                yield self._next()
        except StopIteration:
            pass

    def _next(self) -> T:
        value = next(self._it)
        self._values.append(value)

        return value

