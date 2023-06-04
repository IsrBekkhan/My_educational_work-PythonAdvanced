from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, NumberRange, Length
from re import split

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(validators=[InputRequired(), NumberRange(min=1000000000, max=9999999999)])
    name = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    index = IntegerField()
    comment = StringField()


class TicketForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    family_name = StringField(validators=[InputRequired()])
    ticket = IntegerField(validators=[InputRequired(), NumberRange(min=100000, max=999999)])


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone, name = form.email.data, form.phone.data, form.name.data

        name_elements = split(r'[. ]', name)

        if len(name_elements) < 4:
            return f'Неверный формат поля name: {name}', 400

        for elem in name_elements:

            if len(elem) != 0:

                if not elem[0].isupper():
                    return f'Неверный формат поля name: {name}', 400

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


@app.route('/ticket', methods=['POST'])
def happy_ticket():
    form = TicketForm()

    if form.validate_on_submit():
        name, family_name, ticket = form.name.data, form.family_name.data, form.ticket.data

        sum_1 = sum(int(num) for num in str(ticket)[:3])
        sum_2 = sum(int(num) for num in str(ticket)[3:])

        if sum_1 == sum_2:
            return f"Поздравляем вас, {name} {family_name}!"

        return "Неудача. Попробуйте ещё раз!"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
