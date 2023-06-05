"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField()
    timeout = IntegerField()


def run_python_code_in_subproccess(code: str, timeout: int):
    ...


@app.route('/run_code', methods=['POST'])
def run_code():
    ...


if __name__ == '__main__':
    app.run(debug=True)
