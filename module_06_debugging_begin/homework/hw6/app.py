"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask, url_for, render_template
from werkzeug.exceptions import NotFound

from typing import Tuple, List

app = Flask(__name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


@app.errorhandler(NotFound)
def error_handler(exception) -> Tuple[str, int]:
    links = 'Запрашиваемая страница не найдена. Список доступных страниц:'

    for rule in app.url_map.iter_rules():

        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, _external=True)
            links += f'<li><a href="{url}">{rule.endpoint}</a></li>'

    return links, 400


if __name__ == '__main__':
    app.run(debug=True)
