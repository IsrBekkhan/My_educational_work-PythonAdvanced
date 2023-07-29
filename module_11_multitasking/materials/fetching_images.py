import logging
import os
import time
import threading
import multiprocessing
from typing import List

import requests

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

URL: str = 'https://cataas.com/cat'
OUT_PATH: str = 'temp/{}.jpeg'


def get_image(url: str, result_path: str) -> None:
    response: requests.Response = requests.get(url, timeout=(5, 5))
    if response.status_code != 200:
        return
    with open(result_path, 'wb') as ouf:
        ouf.write(response.content)


def load_images_sequential() -> None:
    start: float = time.time()
    for i in range(10):
        get_image(URL, OUT_PATH.format(i))
    logger.info('Done in {:.4}'.format(time.time() - start))


def load_images_multithreading() -> None:
    start: float = time.time()
    threads: List[threading.Thread] = []
    for i in range(10):
        thread = threading.Thread(target=get_image, args=(URL, OUT_PATH.format(i)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logger.info('Done in {:.4}'.format(time.time() - start))


def load_images_multiprocessing() -> None:
    start: float = time.time()
    procs: List[multiprocessing.Process] = []
    for i in range(10):
        proc = multiprocessing.Process(
            target=get_image,
            args=(URL, OUT_PATH.format(i)),
        )
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    logger.info('Done in {:.4}'.format(time.time() - start))


if __name__ == '__main__':
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    load_images_multiprocessing()
