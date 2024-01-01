from typing import Iterator, Generator


def gen_close_method() -> Iterator[int]:
    for i in range(3):
        try:
            yield i
        except GeneratorExit:
            print(f'Exit with {i=}')
            return


g: Generator = gen_close_method()

next(g)
g.close()
