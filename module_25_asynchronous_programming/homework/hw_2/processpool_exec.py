import multiprocessing
from pathlib import Path
from time import time

from requests import Session


URL = 'https://randomfox.ca/images/{}.jpg'
FOXES_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'foxes'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


def get_fox(fox_id: int, client: Session) -> None:
    with client.get(URL.format(fox_id), timeout=10) as response:
        print(response.status_code)
        result = response.content
        write_to_disk(result, fox_id)


def write_to_disk(content: bytes, id_: int):
    file_path = "{}/{}.png".format(OUT_PATH, id_)
    with open(file_path, mode='wb') as f:
        f.write(content)


def main() -> None:
    with Session() as client:
        parameters = [(id_ + 1, client) for id_ in range(FOXES_WE_WANT)]
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.starmap(get_fox, parameters)


if __name__ == '__main__':
    start = time()
    main()
    print('Время выполнения кода:', round(time() - start, 2), 'cек')

