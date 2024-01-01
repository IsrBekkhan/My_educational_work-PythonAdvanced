from typing import Iterator

#%%

def heavy_computation() -> Iterator[int]:
    for i in range(10000000000000000000000000000000000000000):
        yield i ** 2

g = heavy_computation()
for i in range(10):
    print(next(g))