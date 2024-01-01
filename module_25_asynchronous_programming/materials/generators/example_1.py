from typing import Iterator

#%%

def simple_gen() -> Iterator[str]:
    yield 'something'


print(type(simple_gen))
print(type(simple_gen()))