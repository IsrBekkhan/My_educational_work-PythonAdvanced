from math import factorial
from time import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


INPUT_VALUE: int = 10000


def factorial_sum(number: int) -> int:
    return sum(factorial(num) for num in range(number))


def task_execution_with_threadpool():
    pool = ThreadPool(processes=12)
    start = time()
    result = pool.apply_async(factorial_sum, (INPUT_VALUE,))
    pool.close()
    pool.join()
    end = time() - start
    logger.info(f'Функция с потоками отработала за {end}.')


def task_execution_with_processpool():
    pool = Pool(processes=12)
    start = time()
    result = pool.apply_async(factorial_sum, (INPUT_VALUE,))
    pool.close()
    pool.join()
    end = time() - start
    logger.info(f'Функция с процессами отработала за {end}.')


if __name__ == '__main__':
    task_execution_with_threadpool()
    task_execution_with_processpool()