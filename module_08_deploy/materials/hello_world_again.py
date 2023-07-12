from flask import Flask

app = Flask(__name__)


@app.route("/hello/<username>")
def hello_world(username):
    return f"Привет, {username}!"
