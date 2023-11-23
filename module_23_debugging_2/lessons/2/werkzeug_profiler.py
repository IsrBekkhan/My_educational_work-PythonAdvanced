from flask import Flask
import time
from werkzeug.middleware.profiler import ProfilerMiddleware

app = Flask(__name__)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='.')


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


if __name__ == '__main__':
    app.run()
