"""
Ниже представлен endpoint, который принимают в POST массив чисел (в виде json),
сортируют его одним из 3х алгоритмов и возвращают пользователю ответ.
Три применяемых алгоритма сортировки - сортировка пузырьком (bubble sort)
timsort (стандартная сортировка python) и сортировка кучей (heap sort).

Расставьте debug логирование в каждой функции логирования так,
чтобы по логам можно было понять сколько времени выполняется каждая функция.

Какая же сортировка в итоге выполняется быстрее?
"""

import heapq
import json
import logging
from time import time
from typing import List, Callable

from flask import Flask, request

app = Flask(__name__)

logger = logging.getLogger("sort")


def logging_and_time_measurement(func: Callable):
    def wrapped_func(*args):
        logger.debug(f'Запуск функции {func.__name__}: {args}')
        start = time()
        result = func(*args)
        end = time()
        processing_time = end - start
        print(processing_time)
        logger.info(f'Время сортировки: {processing_time}. Результат {result}')
        logger.debug(f'Конец {time()}')

        return result

    return wrapped_func


@logging_and_time_measurement
def bubble_sort(array: List[int]) -> List[int]:
    n = len(array)

    for i in range(n):
        for j in range(i + 1, n):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]

    return array


@logging_and_time_measurement
def tim_sort(array: List[int]) -> List[int]:
    array.sort()

    return array


@logging_and_time_measurement
def heap_sort(array: List[int]) -> List[int]:
    data = []

    for val in array:
        heapq.heappush(data, val)

    return [heapq.heappop(data) for _ in range(len(data))]


algorithms = {
        "bubble": bubble_sort,
        "tim": tim_sort,
        "heap": heap_sort,
}


@app.route("/<algorithm_name>/", methods=["POST"])
def sort_endpoint(algorithm_name: str):
    logger.debug(f"Алгоритм {algorithm_name}")

    if algorithm_name not in algorithms:
        logger.warning(f'Алгоритм с названием {algorithm_name} нет на сервере.')
        return f"Bad algorithm name, acceptable values are {algorithms.keys()}", 400

    form_data = request.get_data(as_text=True)
    logger.debug(f'Тело запроса: {form_data}')

    array = json.loads(form_data)

    result = algorithms[algorithm_name](array)
    logger.debug(f'Результат сортировки: {result}')

    return json.dumps(result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Started sort server")
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
