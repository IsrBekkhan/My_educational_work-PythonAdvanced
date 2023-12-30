from typing import Iterator

import inspect


def get_states() -> Iterator[int]:
    for i in range(3):
        yield i


g = get_states()
print(inspect.getgeneratorstate(g))
next(g)
print(inspect.getgeneratorstate(g))
next(g)
next(g)

try:
    next(g)
except StopIteration:
    pass

print(inspect.getgeneratorstate(g))