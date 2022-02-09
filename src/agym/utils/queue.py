from typing import TypeVar, Generic, Iterator

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self):
        self.size = 0

        self.first_stack: List[T] = []
        self.second_stack: List[T] = []

    def __len__(self) -> int:
        return len(self.first_stack) + len(self.second_stack)

    def __iter__(self) -> Iterator[T]:
        for item in reversed(self.second_stack):
            yield item

        for item in self.first_stack:
            yield item

    def push(self, value: T) -> None:
        self.size += 1

        self.first_stack.append(value)

    def pop(self) -> T:
        if self.size == 0:
            # Neew throw exception
            pass

        self.size -= 1

        if len(self.second_stack) == 0:
            for i in range(len(self.first_stack)):
                self.second_stack.append(self.first_stack.pop())

        return self.second_stack.pop()

    def tail(self) -> T:
        if self.size == 0:
            raise RuntimeError

        if len(self.second_stack) != 0:
            return self.second_stack[-1]
        else:
            return self.first_stack[0]

    def front(self) -> T:
        if self.size == 0:
            raise RuntimeError

        if len(self.first_stack) != 0:
            return self.first_stack[-1]
        else:
            return self.second_stack[0]
