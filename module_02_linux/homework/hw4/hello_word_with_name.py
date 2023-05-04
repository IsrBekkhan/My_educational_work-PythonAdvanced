"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""
import sys

from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/hello-world/<username>')
def hello_world(username: str) -> str:
    # кортеж - лучший спасоб для хранения дней недели (мало памяти, быстродействие, неизменяемость содержимого)
    weekdays_tuple = (
        'понедельника',
        'вторника',
        'среды',
        'четверга',
        'пятницы',
        'субботы',
        'воскресенья'
    )
    weekdays_list = [
        'понедельника',
        'вторника',
        'среды',
        'четверга',
        'пятницы',
        'субботы',
        'воскресенья'
    ]
    weekdays_dict = {
        0: 'понедельника',
        1: 'вторника',
        2: 'среды',
        3: 'четверга',
        4: 'пятницы',
        5: 'субботы',
        6: 'воскресенья'
    }

    print(sys.getsizeof(weekdays_tuple))
    print(sys.getsizeof(weekdays_list))
    print(sys.getsizeof(weekdays_dict))

    weekday = datetime.today().weekday()

    if weekday in (0, 1, 3, 6):
        return f'Привет, {username}. Хорошего {weekdays_tuple[weekday]}!'
    else:
        return f'Привет, {username}. Хорошей {weekdays_tuple[weekday]}!'


if __name__ == '__main__':
    app.run(debug=True)
