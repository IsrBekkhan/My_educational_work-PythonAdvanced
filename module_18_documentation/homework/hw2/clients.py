import json
from random import randint
from multiprocessing.pool import ThreadPool
from time import time

import requests

import logging

logging.basicConfig(level=logging.DEBUG)


class SpeedTest:
    URL: str = 'http://127.0.0.1:5000/api/books'
    TIMEOUT: int = 5

    def __init__(self, requests_amount: int, session: bool, threads: bool):
        self.requests_amount = requests_amount
        if session:
            self.session = requests.Session()
            if threads:
                self.result = self.__with_session_and_threads()
            else:
                self.result = self.__with_session()
            self.session.close()
        else:
            if threads:
                self.result = self.__without_session()
            else:
                self.result = self.__without_session_and_threads()

    def __str__(self):
        return str(round(self.result, 4))

    def __without_session_and_threads(self):
        logging.debug('СТАРТ ЗАПРОСОВ БЕЗ СЕССИИ И МНОГОПОТОЧНОСТИ')
        start = time()
        for _ in range(self.requests_amount):
            title = 'Secret book №{}'.format(randint(1, 1000000))
            data = {'title': title, 'author_id': 1}
            response = self.__post_request(data)
        logging.debug('ЗАВЕРШЕНИЕ ЗАПРОСОВ БЕЗ СЕССИИ И МНОГОПОТОЧНОСТИ')
        return time() - start

    def __without_session(self):
        logging.debug('СТАРТ ЗАПРОСОВ БЕЗ СЕССИИ НО С МНОГОПОТОЧНОСТЬЮ')
        start = time()
        book_data = [{'title': 'Secret book №{}'.format(randint(1, 1000000)), 'author_id': 1}
                        for _ in range(self.requests_amount)]
        thread_pool = ThreadPool(processes=len(book_data))
        result = thread_pool.map_async(self.__post_request, book_data)
        thread_pool.close()
        thread_pool.join()
        logging.debug('ЗАВЕРШЕНИЕ ЗАПРОСОВ БЕЗ СЕССИИ НО С МНОГОПОТОЧНОСТЬЮ')
        return time() - start

    def __with_session(self):
        logging.debug('СТАРТ ЗАПРОСОВ С ИСПОЛЬЗОВАНИЕМ СЕССИИ БЕЗ МНОГОПОТОЧНОСТИ')
        start = time()
        for _ in range(self.requests_amount):
            title = 'Secret book №{}'.format(randint(1, 1000000))
            data = {'title': title, 'author_id': 1}
            response = self.__session_post(data)
        logging.debug('ЗАВЕРШЕНИЕ ЗАПРОСОВ С ИСПОЛЬЗОВАНИЕМ СЕССИИ БЕЗ МНОГОПОТОЧНОСТИ')
        return time() - start

    def __with_session_and_threads(self):
        logging.debug('СТАРТ ЗАПРОСОВ С ИСПОЛЬЗОВАНИЕМ СЕССИИ И МНОГОПОТОЧНОСТИ')
        start = time()
        book_data = [{'title': 'Secret book №{}'.format(randint(1, 1000000)), 'author_id': 1}
                     for _ in range(self.requests_amount)]
        thread_pool = ThreadPool(processes=len(book_data))
        result = thread_pool.map_async(self.__session_post, book_data)
        thread_pool.close()
        thread_pool.join()
        logging.debug('ЗАВЕРШЕНИЕ ЗАПРОСОВ С ИСПОЛЬЗОВАНИЕМ СЕССИИ И МНОГОПОТОЧНОСТИ')
        return time() - start

    def __post_request(self, data):
        return requests.post(self.URL, json=data, timeout=self.TIMEOUT)

    def __session_post(self, data):
        return self.session.post(self.URL, json=data, timeout=self.TIMEOUT)


if __name__ == '__main__':
    REQUESTS_AMOUNT = 1000

    without_session_and_threads = SpeedTest(REQUESTS_AMOUNT, session=False, threads=False)
    without_session = SpeedTest(REQUESTS_AMOUNT, session=False, threads=True)
    with_session = SpeedTest(REQUESTS_AMOUNT, session=True, threads=False)
    with_session_and_threads = SpeedTest(REQUESTS_AMOUNT, session=True, threads=True)

    print('Результат выполнения без использования сессии и многопоточности: {}'.format(
        without_session_and_threads))
    print('Результат выполнения без использования сессии но с многопоточностью: {}'.format(without_session))
    print('Результат выполнения с использованием сессии без многопоточности: {}'.format(with_session))
    print('Результат выполнения с использованием сессии и многопоточности: {}'.format(
        with_session_and_threads))