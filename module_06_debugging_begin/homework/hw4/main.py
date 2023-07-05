"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import operator
from typing import Dict
from json import loads
from itertools import groupby
from subprocess import run, PIPE


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    levels_count = dict()

    for log in logs:
        level = log['level']

        try:
            levels_count[level] += 1
        except KeyError:
            levels_count[level] = 1

    return levels_count


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    # вариант решения в соответствии с рекомендуемой функцией groupby
    grouped_logs = groupby(logs, key=lambda log: log['time'][:2])

    max_logs_hour = None
    max_logs = 0

    for hour, logs_object in grouped_logs:
        logs_amount = len([elem for elem in logs_object])

        if logs_amount > max_logs:
            max_logs = logs_amount
            max_logs_hour = hour

    return max_logs_hour

    # второй вариант решения с использованием доп. возможностей функции max
    # logs_count = dict()
    #
    # for log in logs:
    #     hour = int(log['time'][:2])
    #
    #     try:
    #         logs_count[hour] += 1
    #     except KeyError:
    #         logs_count[hour] = 1
    #
    # max_hour, count = max(logs_count.items(), key=operator.itemgetter(1))
    #
    # return max_hour


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    command = ['grep', '-c', '"time": "05:[0-1][0-9]:[0-9][0-9]"', 'skillbox_json_messages.log']
    process = run(command, stdout=PIPE, stderr=PIPE)

    return int(process.stdout.decode())


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    command = ['grep', '-c', 'dog', 'skillbox_json_messages.log']
    process = run(command, stdout=PIPE, stderr=PIPE)

    return int(process.stdout.decode())


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    words_count = dict()

    for log in logs:

        if log['level'] == 'WARNING':
            message_words = log['message'].split()

            for word in message_words:
                try:
                    words_count[word] += 1
                except KeyError:
                    words_count[word] = 1

    word, count = max(words_count.items(), key=operator.itemgetter(1))

    return word


if __name__ == '__main__':

    with open('skillbox_json_messages.log', 'r', encoding='utf-8') as log_file:
        logs = [loads(log) for log in log_file.readlines()]

    tasks = (task1, task2, task3, task4, task5)

    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
