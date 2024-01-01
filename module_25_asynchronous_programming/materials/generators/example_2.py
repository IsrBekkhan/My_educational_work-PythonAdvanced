from typing import Iterator

#%%

def simple_gen() -> Iterator[str]:
    yield 'something'


g = simple_gen()
print(g)
print(g.__iter__())
print(g.__next__())
print(g.__next__())