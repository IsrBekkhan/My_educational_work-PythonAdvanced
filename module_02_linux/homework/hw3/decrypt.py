"""
Вася решил передать Пете шифрограмму.
Поскольку о промышленных шифрах Вася ничего не знает,
он решил зашифровать сообщение следующим образом: он посылает Пете строку.

Каждый символ строки — либо буква, либо пробел, либо точка «.», либо две точки «..».
Если после какой-то буквы стоит точка, значит, мы оставляем букву без изменений
(об одной точке Вася задумался, чтобы усложнить расшифровку). Саму точку при этом надо удалить.
Если после какой-то буквы стоят две точки, то предыдущий символ надо стереть. Обе точки при этом тоже нужно удалить.
Возможна ситуация, когда сообщение после расшифровки будет пустым.
В качестве результата можно вернуть просто пустую строку.

Примеры шифровок-расшифровок:

абра-кадабра. → абра-кадабра
абраа..-кадабра → абра-кадабра
абраа..-.кадабра → абра-кадабра
абра--..кадабра → абра-кадабра
абрау...-кадабра → абра-кадабра (сначала срабатывает правило двух точек, потом правило одной точки)
абра........ → <пустая строка>
абр......a. → a
1..2.3 → 23
. → <пустая строка>
1....................... → <пустая строка>

Помогите Пете написать программу для расшифровки.
Напишите функцию decrypt, которая принимает на вход шифр в виде строки, а возвращает расшифрованное сообщение.

Программа должна работать через конвейер (pipe):

$ echo  ‘абраа..-.кадабра’ | python3 decrypt.py
абра-кадабра

Команда echo выводит текст (в стандартный поток вывода).
"""

import sys
from time import time


def decrypt(encryption: str) -> str:
    decrypted_temp = ''

    decrypted_list = encryption.split('..')

    for elem in decrypted_list:

        if len(elem) == 0:

            if len(decrypted_temp) >= 1:
                decrypted_temp = decrypted_temp[:-1]

        else:
            decrypted_temp += elem

    decrypted_list = decrypted_temp.split('.')

    return ''.join(decrypted_list)


def decrypt_2(encryption: str) -> str:
    decrypted = ''
    point_count = 0

    for letter in encryption:

        if letter == '.':
            point_count += 1
        else:
            decrypted += letter

        if point_count == 2:

            if len(decrypted) >= 1:
                decrypted = decrypted[:-1]

            point_count = 0

    return decrypted


def decrypt_3(encryption: str) -> str:
    decrypted_temp = []

    for symbol in encryption:
        decrypted_temp.append(symbol)

        if len(decrypted_temp) > 2 and (decrypted_temp[-1], decrypted_temp[-2]) == ('.', '.'):
            decrypted_temp.pop()
            decrypted_temp.pop()

            if decrypted_temp:
                decrypted_temp.pop()

    return ''.join(symbol for symbol in decrypted_temp if symbol != '.')


if __name__ == '__main__':
    data: str = sys.stdin.read()
    decryption: str = decrypt(data)
    print(decryption)

# Проверил скорость работы всех алгоритм
# Всё же алгоритм №1 намного быстрее, чем алгоритм рассмотренный в разборе домашнего задания)

# word = 'абраа..-.кадабра'
# start = time()
#
# for _ in range(1000000):
#     decrypt(word)
#
# print(time() - start)

