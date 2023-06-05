"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask

import shlex
import subprocess
from typing import Tuple

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> Tuple[str, int]:
    command_str = 'uptime -p'
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True)
    result_str = result.stdout.decode()

    return f'Current uptime is {result_str}.', 200


if __name__ == '__main__':
    app.run(debug=True)
