from typing import Iterator


def get_states() -> Iterator[int]:
    for i in range(3):
        yield i


g = get_states()
print('\n'.join(dir(g)))
