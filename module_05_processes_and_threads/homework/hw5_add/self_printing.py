"""
Напишите код, который выводит сам себя.
Обратите внимание, что скрипт может быть расположен в любом месте.
"""
import sys

result = 0
for n in range(1, 11):
    result += n ** 2


abs_path = sys.argv[0]

with open(abs_path, 'r', encoding='utf-8') as python_file:
    file_text = python_file.readlines()
    print(*file_text)
