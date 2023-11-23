from flask import Flask
import flask.json
import time
import flask_profiler
import decimal

from sqlalchemy import create_engine

engine = create_engine('sqlite:///flask_profiler.db')

app = Flask(__name__)


@app.route("/one")
def one():
    return "one"


@app.route("/two")
def two():
    time.sleep(10)
    return "two"


@app.route("/three")
def three():
    l = []
    for i in range(1000000):
        l.append(i)
    return "three"


@app.route("/four")
def four():
    return "four"


app.config["flask_profiler"] = {
    "enabled": True,

    "storage": {
        "engine": "sqlalchemy",
        "db_url": "sqlite:///flask_profiler.db"
    },
    "basicAuth": {
        "enabled": True,
        "username": "admin",
        "password": "admin"
    }

}
flask_profiler.init_app(app)


class NewEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(NewEncoder, self).default(o)


app.json_encoder = NewEncoder


# в случае, если роут описан после flask_profiler.init_app(app), необходимо
# применить декоратор, иначе он не будет обрабатываться профайлером
@app.route('/five', methods=['GET'])
@flask_profiler.profile()
def five():
    return "five"


if __name__ == '__main__':
    app.run()
