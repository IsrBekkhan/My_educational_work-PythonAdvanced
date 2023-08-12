import threading
import multiprocessing
import logging
import requests
import time
import os
from typing import List


logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

URL: str = 'https://cataas.com/cat'
OUT_PATH: str = 'temp/{}.jpeg'
max_processes: int = 22


def get_image(url: str, result_path: str) -> None:
    response: requests.Response = requests.get(url, timeout=(5, 5))
    if response.status_code != 200:
        return
    with open(result_path, 'wb') as ouf:
        ouf.write(response.content)


def task(number: int) -> int:
    return sum(i ** i for i in range(number))


def load_images_sequential() -> None:
    start: float = time.time()
    for i in range(max_processes):
        get_image(URL, OUT_PATH.format(i))
    logger.info('Sequential done in {:.4}'.format(time.time() - start))


def load_images_multithreading() -> None:
    start: float = time.time()
    threads: List[threading.Thread] = []
    for i in range(max_processes):
        thread = threading.Thread(target=get_image, args=(URL, OUT_PATH.format(i)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logger.info('Threading_done in {:.4}'.format(time.time() - start))


def load_images_multiprocessing() -> None:
    start: float = time.time()
    procs: List[multiprocessing.Process] = []
    for i in range(max_processes):
        proc = multiprocessing.Process(
            target=get_image,
            args=(URL, OUT_PATH.format(i)),
        )
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    logger.info('Multiprocessing_done in {:.4}'.format(time.time() - start))


def run_multiprocessing():
    start: float = time.time()
    procs: List[multiprocessing.Process] = []

    for i in range(max_processes):
        proc = multiprocessing.Process(target=task, args=(i, ))
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    logger.info('Multiprocessing_done in {:.4}'.format(time.time() - start))


def run_multithreading():
    start: float = time.time()
    threads: List[threading.Thread] = []

    for i in range(max_processes):
        thread = threading.Thread(target=task, args=(i, ))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logger.info('Multiprocessing_done in {:.4}'.format(time.time() - start))


if __name__ == '__main__':

    if not os.path.exists('./temp'):
        os.mkdir('./temp')

    # load_images_sequential()
    # load_images_multiprocessing()
    # load_images_multithreading()

    run_multiprocessing()
    run_multithreading()
