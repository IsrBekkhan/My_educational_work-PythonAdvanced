from flask import Flask, jsonify

from typing import Tuple, Callable

from database import POSTGRES_URL


app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello() -> Tuple[Callable, int]:
    return jsonify(message='Hello World!'), 200


@app.route('/db_url', methods=['GET'])
def db_url() -> Tuple[Callable, int]:
    return jsonify(db_url=POSTGRES_URL), 200
