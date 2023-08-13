import time
import logging
import os
import multiprocessing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MySuperClass(object):

    def __init__(self, name):
        self.name = name

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        proc_pid = os.getpid()
        logger.info(f'Doing something fancy in {proc_name}, pid {proc_pid} for {self.name}!')


def worker(queue: multiprocessing.Queue):
    while not queue.empty():
        obj = queue.get()
        obj.do_something()
        time.sleep(0.1)


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    pool = multiprocessing.Pool(
        processes=multiprocessing.cpu_count(),
        initializer=worker,
        initargs=(queue,)
    )

    for i in range(1, 40):
        queue.put(MySuperClass(f'Object num {i}'))

    # prevent adding anything more to the queue and wait for queue to empty
    queue.close()
    queue.join_thread()

    # prevent adding anything more to the process pool and wait for all
    # processes to finish
    pool.close()
    pool.join()
