"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min_len: int, max_len: int, message: Optional[str] = None):

    if message:
        error_message = message
    else:
        error_message = f'Длина числа не может быть меньше {max_len} и больше {max_len}.'

    def _number_length(form: FlaskForm, field: Field):

        if len(str(field.data)) > max_len or len(str(field.data)) < min_len:
            raise ValidationError(error_message)

    return _number_length


class NumberLength:
    def __init__(self, min_len: int, max_len: int, message: Optional[str] = None):
        self.min = min_len
        self.max = max_len

        if message:
            self.message = message
        else:
            self.message = f'Длина числа не может быть меньше {max_len} и больше {max_len}.'

    def __call__(self, form: FlaskForm, field: Field):

        if len(str(field.data)) > self.max or len(str(field.data)) < self.min:
            raise ValidationError(self.message)