import asyncio
import time
from typing import Union


@asyncio.coroutine
def print_two_powers(name: str, limit: int, frequency: Union[int, float] = 1):
    for i in range(limit):
        print(name, 2 ** i)
        yield from asyncio.sleep(frequency)
    else:
        print("Done")


@asyncio.coroutine
def coroutine_1():
    yield from print_two_powers('Worker_1', 3, 0.1)


@asyncio.coroutine
def coroutine_2():
    yield from print_two_powers('Worker_2', 5, 0.5)


@asyncio.coroutine
def main():
    task1 = asyncio.create_task(coroutine_1())
    task2 = asyncio.create_task(coroutine_2())
    yield from task1
    yield from task2


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)
