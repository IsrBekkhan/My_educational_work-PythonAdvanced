"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys
from typing import Union


def get_mean_size(ls_output: str) -> Union[float, str]:
    average_size = 0
    files_amount = 0

    for line in ls_output:

        if not line.startswith('d'):
            line_elements = line.split()
            files_amount += 1
            try:
                average_size += int(line_elements[4])
            except ValueError:
                print(f'не удалось получить размер файла {line_elements[8]}')

    if files_amount == 0:
        return 'в данном каталоге нет файлов'

    return round(average_size / files_amount, 2)


if __name__ == '__main__':
    data: str = sys.stdin.readlines()[1:]
    mean_size: float = get_mean_size(data)
    print(mean_size)
