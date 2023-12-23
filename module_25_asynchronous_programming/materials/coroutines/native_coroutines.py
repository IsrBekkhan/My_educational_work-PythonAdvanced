import asyncio
import time
from typing import Union


async def print_two_powers(name: str, limit: int, frequency: Union[int, float] = 1):
    for i in range(limit):
        print(name, 2 ** i)
        await asyncio.sleep(frequency)
    else:
        print("Done")


async def coroutine_1():
    return await print_two_powers('Worker_1', 3, 0.1)


async def coroutine_2():
    return await print_two_powers('Worker_2', 5, 0.5)


async def main():
    task1 = asyncio.create_task(coroutine_1())
    task2 = asyncio.create_task(coroutine_2())
    await task1
    await task2


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)
