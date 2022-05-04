from typing import List, TypeVar, Generic, Iterator

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self):
        self.front_stack: List[T] = []
        self.back_stack: List[T] = []

    def push(self, value: T) -> None:
        self.front_stack.append(value)

    def pop(self) -> T:
        if self.size == 0:
            raise RuntimeError("Queue is empty and value cannot be poped")

        if len(self.back_stack) == 0:
            for i in range(len(self.front_stack)):
                self.back_stack.append(self.front_stack.pop())

        return self.back_stack.pop()

    @property
    def back(self) -> T:
        if self.size == 0:
            raise RuntimeError("Queue is empty and has no tail")

        if len(self.back_stack) != 0:
            return self.back_stack[-1]
        else:
            return self.front_stack[0]

    @property
    def front(self) -> T:
        if self.size == 0:
            raise RuntimeError("Queue is empty and has no front")

        if len(self.front_stack) != 0:
            return self.front_stack[-1]
        else:
            return self.back_stack[0]

    @property
    def size(self) -> int:
        return len(self)

    def __len__(self) -> int:
        return len(self.front_stack) + len(self.back_stack)

    def __iter__(self) -> Iterator[T]:
        for item in reversed(self.back_stack):
            yield item

        for item in self.front_stack:
            yield item
