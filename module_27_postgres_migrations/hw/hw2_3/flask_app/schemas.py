from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    coffee_id = IntegerField(validators=[InputRequired()])
