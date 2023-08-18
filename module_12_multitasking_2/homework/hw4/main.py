from queue import Queue
from threading import Thread, Lock
from time import sleep, time
import logging
import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler('something_happening.log', mode='a', encoding='utf-8'))
logger.setLevel(logging.INFO)

THREAD_WORK_TIME = 20
THREADS_AMOUNT = 10


def log_writer(lock: Lock):
    while True:
        with lock:
            timestamp = time()
            response = requests.get(f'http://127.0.0.1:8080/timestamp/{timestamp}')
            logger.info(f'Timestamp: {timestamp}; Data: {response.content.decode()}')
            sleep(1)


def worker(queue: Queue):
    while not queue.empty():
        thread_obj: Thread = queue.get()
        thread_obj.start()
        start_ = time()
        thread_obj.join(THREAD_WORK_TIME)
        print(f'Время работы потока {round(time() - start_, 2)} сек.')
        sleep(1)


if __name__ == '__main__':
    queue_ = Queue()
    locker = Lock()

    for _ in range(THREADS_AMOUNT):
        thread = Thread(target=log_writer, args=(locker,), daemon=True)
        queue_.put(thread)

    start = time()
    worker(queue_)
    work_time = round(time() - start, 2)
    logger.info(f'Время работы программы {work_time} сек')
