import time
import logging
import multiprocessing
from multiprocessing.pool import ThreadPool

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_VALUES = [
    'https://en.wikipedia.org/wiki/Main_Page',
    'https://en.wikipedia.org/wiki/Python_(programming_language)',
] * 20


def task(url: str):
    response = requests.get(url, timeout=(5, 5))
    return len(response.content)


def task_execution_with_threadpool():
    pool = ThreadPool(processes=multiprocessing.cpu_count() * 5)
    start = time.time()
    result = pool.map(task, INPUT_VALUES)
    pool.close()
    pool.join()
    end = time.time()
    logger.info(f'Time taken in seconds with threadpool - {end - start}')


def sequential_approach():
    start = time.time()
    for inp in INPUT_VALUES:
        task(inp)
    end = time.time()
    logger.info(f'Time taken in seconds for sequential - {end - start}')


def task_execution_with_processpool():
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start = time.time()
    result = pool.map(task, INPUT_VALUES)
    pool.close()
    pool.join()
    end = time.time()
    logger.info(f'Time taken in seconds with processes pool - {end - start}')


if __name__ == '__main__':
    sequential_approach()
    task_execution_with_threadpool()
    task_execution_with_processpool()
