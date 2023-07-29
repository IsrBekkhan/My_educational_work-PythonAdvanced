import random
import threading
import time

from threading import Lock

COUNTER: int = 1
LOCK: threading.Lock = Lock()


def worker_one() -> None:
    global COUNTER
    with LOCK:
        while COUNTER < 1000:
            COUNTER += 1

            print(f'Worker one incremented counter to {COUNTER}')
            sleep_time: int = random.randint(0, 1)
            time.sleep(sleep_time)


def worker_two():
    global COUNTER
    with LOCK:
        while COUNTER > -1000:
            COUNTER -= 1

            print(f'Worker two decremented counter to {COUNTER}')
            sleep_time: int = random.randint(0, 1)
            time.sleep(sleep_time)


def main():
    start = time.time()
    thread_1 = threading.Thread(target=worker_one)
    thread_2 = threading.Thread(target=worker_two)
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()
    print('Execution time {:.4}'.format(time.time() - start))


if __name__ == '__main__':
    main()
