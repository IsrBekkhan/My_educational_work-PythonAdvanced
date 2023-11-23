from my_flask import SimplestWSGIApp
import json
import time
from flask import jsonify


application = SimplestWSGIApp()


@application.route("/hello/<name>")
def hello_world(name: str):
    return json.dumps({"response": f"Hello, {name}!"}, indent=4, ensure_ascii=True), 200


@application.route('/long_task')
def long_task():
    time.sleep(300)
    return json.dumps({'message': 'We did it!'}), 200
