"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
from typing import List
from re import findall


phone_keys = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz'
}


def my_t9(input_numbers: str) -> List[str]:
    pattern = ''

    for number in input_numbers:

        if number == '1' or number == '0':
            continue

        letters: str = phone_keys[number]
        pattern_path = f'[{letters}{letters.upper()}]'
        pattern += pattern_path

    word_length = len(input_numbers)
    found_words = list()

    with open('../hw1_2/words.txt', 'r') as words_file:

        for word in words_file.readlines():

            if len(word.rstrip()) == word_length:

                result = findall(pattern, word)

                if result:
                    found_words.append(*result)
    return found_words


if __name__ == '__main__':
    numbers: str = input()
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')
