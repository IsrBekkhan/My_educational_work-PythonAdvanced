"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, NumberRange
from hw2_validators import number_length, NumberLength

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email_error_message = 'Введенное значение не является эл.почтой.'
    phone_error_message = 'Неверный номер телефона.'
    required_error_message = 'Это поле обязательно к заполнению'

    email = StringField(validators=[
        InputRequired(message=required_error_message),
        Email(message=email_error_message)
    ])
    phone = IntegerField(validators=[
        InputRequired(message=required_error_message),
        NumberLength(min_len=10, max_len=10, message=phone_error_message
                     )])
    name = StringField(validators=[
        InputRequired(message=required_error_message)
    ])
    address = StringField(validators=[
        InputRequired(message=required_error_message)
    ])
    index = IntegerField(validators=[
        InputRequired(message=required_error_message)
    ])
    comment = StringField(validators=[
        InputRequired(message=required_error_message)
    ])


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
