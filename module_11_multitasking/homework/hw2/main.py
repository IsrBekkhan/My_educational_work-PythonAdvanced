from requests import Response, get
import sqlite3
from logging import basicConfig, INFO, getLogger, Logger
from time import time
from threading import Thread
from typing import List


basicConfig(level=INFO)
logger: Logger = getLogger(__name__)


def get_person(person_id: int):
    logger.info(f"Запрос данных персонажа с номером {person_id}")
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


def consistent_request() -> float:
    logger.info(f"Последовательный запрос функцией {consistent_request.__name__}")
    start = time()

    for number in range(1, 21):
        get_person(number)

    logger.info('Завершение последовательного запроса')
    return round(time() - start, 3)


def parallel_request() -> float:
    logger.info(f"Параллельный запрос функцией {parallel_request.__name__}")
    start = time()

    threads: List[Thread] = []

    for number in range(1, 21):
        thread = Thread(target=get_person, args=(number, ))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logger.info('Завершение параллельного запроса')
    return round(time() - start, 3)


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

    consist_time = consistent_request()
    parallel_time = parallel_request()
    logger.info(f"Время последовательного запроса {consist_time} сек.")
    logger.info(f"Время параллельного запроса {parallel_time} сек.")
