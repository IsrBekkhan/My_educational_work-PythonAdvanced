from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email


class SubscribeForm(FlaskForm):
    email_error_message = 'Введенное значение не является эл.почтой.'
    required_error_message = 'Это поле обязательно к заполнению'

    email = StringField(validators=[
        InputRequired(message=required_error_message),
        Email(message=email_error_message)
    ])
