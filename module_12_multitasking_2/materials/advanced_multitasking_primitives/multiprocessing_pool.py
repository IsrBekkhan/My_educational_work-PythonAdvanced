import time
import logging
from multiprocessing import Pool, cpu_count

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def task(number):
    return sum(i ** i for i in range(number))


def apply_async():
    pool = Pool(processes=2)
    start = time.time()
    input_value = 1000
    result_1 = pool.apply_async(task, [input_value // 2])
    result_2 = pool.apply_async(task, [input_value // 2])
    pool.close()
    pool.join()

    logger.info(result_1)
    logger.info(result_2.get(timeout=1))

    end = time.time()
    logger.info(f'Time taken in seconds - {end - start}')


def map():
    pool = Pool(processes=2)
    start = time.time()
    input_values = [500, 500]
    result = pool.map_async(task, input_values)
    pool.close()
    pool.join()
    logger.info(result)
    logger.info(result.get(timeout=1))
    end = time.time()
    logger.info(f'Time taken in seconds - {end - start}')


def high_load_map():
    start = time.time()
    input_value = [i for i in range(1, 1000, 100)]

    with Pool(processes=cpu_count()) as pool:
        result = pool.map(task, input_value)

    end = time.time()
    logger.info(f'Time taken in seconds - {end - start}')
    logger.info(len(result))


if __name__ == '__main__':
    high_load_map()
