import asyncio
from pathlib import Path
from time import time

import aiofiles
import aiohttp


URL = 'https://randomfox.ca/images/{}.jpg'
FOXES_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'foxes'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def get_fox(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL.format(idx)) as response:
        print(response.status)
        result = await response.read()
        await write_to_disk(result, idx)


async def write_to_disk(content: bytes, id_: int):
    file_path = "{}/{}.png".format(OUT_PATH, id_)
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)


async def get_all_foxes():

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_fox(client, i + 1) for i in range(FOXES_WE_WANT)]
        return await asyncio.gather(*tasks)


def main():
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Для запуска кода на Windows
    # Обуждение вопроса: https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    res = asyncio.run(get_all_foxes())
    print(len(res))


if __name__ == '__main__':
    start = time()
    main()
    print('Время выполнения кода:', round(time() - start, 2), 'cек')
