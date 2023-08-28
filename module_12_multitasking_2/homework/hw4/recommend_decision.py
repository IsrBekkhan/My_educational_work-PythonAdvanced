from typing import Optional
import requests
import threading
from queue import Queue
import datetime
import logging
import time


URL: str = 'http://127.0.0.1:8080/timestamp/{}'
WORKERS_COUNT: int = 10
WORKER_REQUESTS: int = 20

queue: Queue = Queue(WORKERS_COUNT * WORKER_REQUESTS)
data: dict[float, Optional[str]] = {}


def get_date(timestamp: float) -> str:
    return requests.get(URL.format(timestamp)).text


class Worker(threading.Thread):
    def run(self) -> None:
        for _ in range(WORKER_REQUESTS):
            timestamp: float = datetime.datetime.now().timestamp()
            data[timestamp] = None

            queue.put(timestamp)
            date: str = get_date(timestamp)
            data[timestamp] = date

            time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(
        level='INFO',
        filename='sorted_logs.log',
        format='%(asctime)s | %(message)s'
    )

    threads: list[Worker] = []

    for i in range(WORKERS_COUNT):
        thread: Worker = Worker()
        thread.start()
        threads.append(thread)
        time.sleep(1)

    for i in range(queue.qsize()):
        timestamp: float = queue.get()
        while data.get(timestamp) is None:
            continue
        logging.info(f'{timestamp} -- {data[timestamp]}')

    for thread in threads:
        thread.join()