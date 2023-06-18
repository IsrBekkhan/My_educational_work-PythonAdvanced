import math

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField
from wtforms.validators import InputRequired

app = Flask(__name__)


class Formula1Form(FlaskForm):
    x = FloatField(validators=[InputRequired()])


class Formula2Form(FlaskForm):
    x = FloatField(validators=[InputRequired()])
    n = IntegerField(validators=[InputRequired()])


@app.route("/formula1/", methods=["POST"])
def formula1():
    form = Formula1Form()

    if form.validate_on_submit():
        x: float = form.x.data

        result = math.sin(x) / x

        return f"sin({x}) / {x} = {result}"

    return f"Bad request. Error = {form.errors}", 400


@app.route("/formula2/", methods=["POST"])
def formula2():
    form = Formula2Form()

    if form.validate_on_submit():
        x, n = form.x.data, form.n.data

        result: float = 0.0

        for i in range(1, n + 1):
            result += 1.0 / (i * x)

        return f"Your result is {result}"

    return f"Bad request. Error = {form.errors}", 400


@app.errorhandler(ZeroDivisionError)
def handle_exception(e: ZeroDivisionError):
    return "We are unable to divide by zero!", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run()
