from flask import Flask

import datetime
from random import choice
import os
from re import findall

app = Flask(__name__)

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats_list = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

counter = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

with open(BOOK_FILE, 'r', encoding='utf-8') as book:
    book_file = book.read()
    words_list = findall(r'[а-яА-Я]+', book_file)


@app.route('/hello_world')
def hello_world_func():
    return 'Привет, мир!'


@app.route('/cars')
def cars_list_func():
    return ', '.join(cars_list)


@app.route('/cats')
def random_cat_func():
    return choice(cats_list)


@app.route('/get_time/now')
def time_display_func():
    current_time = str(datetime.datetime.now().time())
    return 'Точное время: {current_time}'.format(current_time=current_time)


@app.route('/get_time/future')
def future_time_display_func():
    future_datetime = datetime.datetime.now() + datetime.timedelta(hours=1)
    future_time = str(future_datetime.time())
    return 'Точное время через час будет {current_time_after_hour}'.format(
        current_time_after_hour=future_time
    )


@app.route('/get_random_word')
def get_random_word_func():
    return choice(words_list)


@app.route('/counter')
def counter_func():
    global counter
    counter += 1
    return 'Данная страница открывалась {count} раз(a).'.format(count=counter)


if __name__ == '__main__':
    app.run(debug=True)
