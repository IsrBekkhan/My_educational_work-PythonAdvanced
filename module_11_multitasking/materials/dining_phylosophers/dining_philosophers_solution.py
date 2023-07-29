import logging
import threading
import random
import time
from typing import List

logging.basicConfig(level='INFO')
logger: logging.Logger = logging.getLogger(__name__)


class Philosopher(threading.Thread):
    running: bool = True  # used to check if everyone is finished eating

    def __init__(self, left_fork: threading.Lock, right_fork: threading.Lock) -> None:
        super().__init__()
        self.left_fork: threading.Lock = left_fork
        self.right_fork: threading.Lock = right_fork

    def run(self) -> None:
        while self.running:
            logger.info(f'Philosopher {self.name} start thinking.')
            # Philosopher is thinking (but really is sleeping).
            time.sleep(random.randint(1, 10))
            logger.info(f'Philosopher {self.name} is hungry.')
            try:
                self.left_fork.acquire()
                logger.info(f'Philosopher {self.name} acquired left fork')
                if self.right_fork.locked():
                    continue
                try:
                    self.right_fork.acquire()
                    logger.info(f'Philosopher {self.name} acquired right fork')
                    self.dining()
                finally:
                    self.right_fork.release()
            finally:
                self.left_fork.release()

    def dining(self) -> None:
        logger.info(f'Philosopher {self.name} starts eating.')
        time.sleep(random.randint(1, 10))
        logger.info(f'Philosopher {self.name} finishes eating and leaves to think.')


def main() -> None:
    forks: List[threading.Lock] = [threading.Lock() for n in range(5)]  # initialising array of Lock's i.e forks

    # here (i+1)%5 is used to get right and left forks circularly between 1-5
    philosophers: List[Philosopher] = [
        Philosopher(forks[i % 5], forks[(i + 1) % 5])
        for i in range(5)
    ]
    Philosopher.running = True
    for p in philosophers:
        p.start()
    time.sleep(200)
    Philosopher.running = False
    logger.info("Now we're finishing.")


if __name__ == "__main__":
    main()
