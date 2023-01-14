import datetime
from flask import Flask

app = Flask(__name__)


@app.route('/hello_world')
def test_function():
    pass


@app.route('/cars')
def test_function():
    pass


@app.route('/cats')
def test_function():
    pass


@app.route('/get_time/now')
def test_function():
    pass


@app.route('/get_time/future')
def test_function():
    pass


@app.route('/get_random_word')
def test_function():
    pass


@app.route('/counter')
def test_function():
    pass


if __name__ == '__main__':
    app.run(debug=True)
