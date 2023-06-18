"""
Представим, что мы работаем в IT отделе крупной компании.
У HR отдела появилась гениальная идея - поздравлять сотрудников
в день рождения однодневным отгулом.

Для этого HR отделу надо предоставить данные на всех
сотрудников вместе с их датами рождения.
Сотрудники у нас работают либо в IT-, либо в PROD-отделе.
Идентификационным номером сотрудника является число,
анкеты сотрудников в формате json вы можете найти в папке fixtures.
В написанное приложение добавьте логи так,
чтобы они помогли найти ошибки со следующими сотрудниками
    отдел IT, сотрудники 1, 2, 3, 4, 5
    отдел PROD, сотрудники 1, 2, 3, 4, 5
"""

import json
import logging
import os

from flask import Flask

app = Flask(__name__)

logger = logging.getLogger("account_book")

current_dir = os.path.dirname(os.path.abspath(__file__))
fixtures_dir = os.path.join(current_dir, "fixtures")

departments = {"IT": "it_dept", "PROD": "production_dept"}


@app.route("/account/<department>/<int:account_number>/")
def account(department: str, account_number: int):
    dept_directory_name = departments.get(department)

    if dept_directory_name is None:
        return "Department not found", 404

    full_department_path = os.path.join(fixtures_dir, dept_directory_name)

    account_data_file = os.path.join(full_department_path, f"{account_number}.json")

    with open(account_data_file, "r") as fi:
        account_data_txt = fi.read()

    account_data_json = json.loads(account_data_txt)

    name, birth_date = account_data_json["name"], account_data_json["birth_date"]
    day, month, _ = birth_date.split(".")
    return f"{name} was born on {day}.{month}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Started account server")
    app.run(debug=True)
