import os

from flask import Flask

app = Flask(__name__)


@app.route("/hello/<username>")
def hello_world(username):
    return f"Привет, {username}!"


@app.route("/even/<int:number>")
def even(number: int):
    if number % 2:
        res = "odd"
    else:
        res = "even"

    return f"The number {number} is <b>{res}</b>"


@app.route("/compare/<float:number_1>/<float:number_2>")
def compare(number_1: float, number_2: float):
    if number_1 < number_2:
        result = "<"
    elif number_1 > number_2:
        result = ">"
    else:
        result = "=="

    return f"<h3>Compare</h3> {number_1} {result} {number_2}"


@app.route("/check_exists/<path:file_path>")
def check_exists(file_path):
    """
    Check if file with relative path exists in file system

    :param file_path: the relative path
    :return: http response
    """
    file_exists = os.path.exists(file_path)
    result = "exists" if file_exists else "does not exist"
    status_code = 200 if file_exists else 404

    return f"File <i>{file_path}</i> {result}", status_code


if __name__ == "__main__":
    app.run(debug=True)
