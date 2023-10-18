from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired, NumberRange


class BookForm(FlaskForm):

    book_id = IntegerField(validators=[
        InputRequired(message='Не указан book_id!'),
        NumberRange(min=0)
    ])
    student_id = IntegerField(validators=[
        InputRequired(message='Не указан student_id!'),
        NumberRange(min=0)
    ])
