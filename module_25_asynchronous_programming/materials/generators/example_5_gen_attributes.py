import inspect
from typing import Iterator, Generator


def get_states() -> Iterator[int]:
    for i in range(3):
        yield i


g: Generator = get_states()

next(g)
g.close()
print(inspect.getgeneratorstate(g))
next(g)

