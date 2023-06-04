"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

from flask import Flask, request

import shlex
import subprocess

from typing import List, Tuple

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> Tuple[str, int]:
    args: List[str] = request.args.getlist('arg')

    user_cmd = ''.join(args)
    clear_user_cmd = shlex.quote(user_cmd)
    command_str = f'ps {clear_user_cmd}'

    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True)
    result_str = result.stdout.decode()

    return f'<pre>{result_str}</pre>', 200


if __name__ == "__main__":
    app.run(debug=True)
