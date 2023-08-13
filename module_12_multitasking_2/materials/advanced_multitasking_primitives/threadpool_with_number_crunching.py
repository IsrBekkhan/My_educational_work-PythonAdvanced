import time
import logging
import multiprocessing
from multiprocessing.pool import ThreadPool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_VALUES = [5000000] * 10


def task(number: int):
    return sum(i * i for i in range(number))


def task_execution_with_threadpool():
    pool = ThreadPool(processes=5)
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
    pool = multiprocessing.Pool(processes=5)
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
