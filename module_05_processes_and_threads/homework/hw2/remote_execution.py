"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import subprocess

from flask import Flask
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

from typing import Tuple

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[
        InputRequired(),
        NumberRange(min=1, max=30)
    ])


def run_python_code_in_subprocess(code: str, timeout: int) -> Tuple[str, int]:
    command = 'prlimit --nproc=1:1 python3 -c "{}"'.format(code)

    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:

        try:
            stdout, stderr = process.communicate(timeout=timeout)

            if stderr:
                return stderr.decode(), process.returncode

        except subprocess.TimeoutExpired:
            return 'Превышено время ожидания исполнения введённого кода.', process.returncode
        else:
            return stdout.decode(), process.returncode


@app.route('/run_code', methods=['POST'])
def run_code() -> Tuple[str, int]:
    code_form = CodeForm()

    if code_form.validate_on_submit():
        code, timeout = code_form.code.data, code_form.timeout.data

        result, return_code = run_python_code_in_subprocess(code, timeout)

        if return_code is None:
            return result, 400
        elif return_code == 0:
            return result, 200
        else:
            return result, 400

    return f"Неверный ввод: {code_form.errors}", 400


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)


