import logging
import random
import threading
import time

TOTAL_TICKETS = 100
AVAILABLE_TICKET = 10

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super(Director, self).__init__()
        self.lock = semaphore
        logger.info('Director started work')

    def run(self):
        global TOTAL_TICKETS, AVAILABLE_TICKET
        while TOTAL_TICKETS:
            if AVAILABLE_TICKET < 4:
                with self.lock:
                    tickets_to_print = 10 - (AVAILABLE_TICKET % 10)
                    if tickets_to_print > TOTAL_TICKETS:
                        tickets_to_print = TOTAL_TICKETS
                    AVAILABLE_TICKET += tickets_to_print
                    TOTAL_TICKETS -= tickets_to_print
                    logger.info(f'Director put {tickets_to_print} new tickets')
        logger.info('Director stops work, not more tickets left.')


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.getName()} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


def main():
    semaphore = threading.Semaphore()
    director = Director(semaphore=semaphore)
    director.start()
    sellers = [director]
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
