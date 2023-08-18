from requests import Response, get
import sqlite3
from logging import basicConfig, INFO, getLogger, Logger
from time import time
from multiprocessing.pool import Pool, ThreadPool
from multiprocessing import cpu_count
from random import randint


basicConfig(level=INFO)
logger: Logger = getLogger(__name__)

INPUT_VALUES = [randint(1, 50) for _ in range(20)]


def get_person(person_id: int) -> None:
    logger.info(f'Запрос данных персонажа с номером {person_id}')
    url = f'https://swapi.dev/api/people/{person_id}'
    response: Response = get(url)

    if response.status_code == 200:
        name, age, gender = response.json()['name'], response.json()['birth_year'], response.json()['gender']
        logger.info(f'Данные персонажа {person_id}: имя - {name}, возраст - {age}, пол - {gender}')

        with sqlite3.connect('star_wars_people.db') as connect_:
            logger.info(f'Добавление данных персонажа {person_id} в БД')
            cursor_ = connect_.cursor()
            query = "INSERT INTO SW_people(name, age, gender)"\
                    "VALUES('{}', '{}', '{}')".format(name, age, gender)
            cursor_.execute(query)


def pool_decision() -> float:
    logger.info('Начало работы функции с использованием Pool')

    pool = Pool(processes=cpu_count())
    start = time()
    result = pool.map_async(get_person, INPUT_VALUES)
    pool.close()
    pool.join()

    logger.info('Завершение работы функции с использованием Pool')
    return time() - start

def threadpool_decision():
    logger.info('Начало работы функции с использованием ThreadPool')

    thread_pool = ThreadPool(processes=len(INPUT_VALUES))
    start = time()
    result = thread_pool.map_async(get_person, INPUT_VALUES)
    thread_pool.close()
    thread_pool.join()

    logger.info('Завершение работы функции с использованием ThreadPool')
    return time() - start


if __name__ == '__main__':

    with sqlite3.connect('star_wars_people.db') as connect:
        cursor = connect.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS SW_people("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT,"
            "age TEXT,"
            "gender TEXT)"
        )

    pool_time = pool_decision()
    threadpool_time = threadpool_decision()
    logger.info(f"Время работы с Pool {pool_time} сек.")
    logger.info(f"Время работы с ThreadPool {threadpool_time} сек.")
